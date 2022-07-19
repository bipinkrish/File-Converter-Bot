#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import logging
import math
import os
import statistics
import signal
import sys

from argparse import RawTextHelpFormatter
from halo import Halo
from wand.api import library
from wand.color import Color
from wand.compat import nested
from wand.image import Image


BLACK_POINT_PRESETS = {
    "lomography-color-tiger": {
        "exposure_gamma_correction": 1.0,
        "r_shift": 379.4375,
        "g_shift": 13485.75390625,
        "b_shift": 32497.3515625,
        "is_black_and_white": False,
        "shift_color_channels": True,
    },
    "kodak-portra-800": {
        "exposure_gamma_correction": 1.0,
        "r_shift": 6156.09765625,
        "g_shift": 27330.96875,
        "b_shift": 46130.76953125,
        "is_black_and_white": False,
        "shift_color_channels": False,
    },
}


def signal_handler(sig, frame):
    sys.exit(0)


class Film(object):
    def __init__(
        self,
        negative,
        positive,
        blackref_preset,
        blackref,
        save_blackref,
        border_size,
        ignore_border_left,
        ignore_border_right,
        ignore_border_top,
        ignore_border_bottom,
        contrast,
        clipping_fuzz_black,
        clipping_fuzz_white,
        save_jpeg,
        save_flip,
        save_flop,
        shift_channels,
        bw_autodetect_off,
        verbose,
    ):
        self.negative = negative
        self.positive = positive
        self.blackref = blackref
        self.save_blackref = save_blackref
        self.border_size = border_size
        self.use_left_border = not ignore_border_left
        self.use_right_border = not ignore_border_right
        self.use_top_border = not ignore_border_top
        self.use_bottom_border = not ignore_border_bottom
        self.contrast = contrast
        self.clipping_fuzz_black = clipping_fuzz_black
        self.clipping_fuzz_white = clipping_fuzz_white
        self.save_jpeg = save_jpeg
        self.save_flip = save_flip
        self.save_flop = save_flop
        self.shift_color_channels = shift_channels
        self.bw_autodetect_off = bw_autodetect_off

        if self.save_jpeg:
            positive_no_extension = os.path.splitext(self.positive)[0]
            self.positive = f"{positive_no_extension}.jpg"

        if (
            (not self.use_left_border)
            and (not self.use_right_border)
            and (not self.use_top_border)
            and (not self.use_bottom_border)
        ):
            self.use_left_border = True
            self.use_right_border = True
            self.use_top_border = True
            self.use_bottom_border = True

        self.temp_blackref_image = "_blackref.jpg"
        self.image_channel = "gray"

        self.exposure_gamma_correction = 1.0
        self.r_shift = 0.0
        self.g_shift = 0.0
        self.b_shift = 0.0

        if verbose:
            logging.basicConfig(format="%(message)s", level=logging.INFO)
        else:
            logging.basicConfig(format="%(message)s", level=logging.WARNING)

        self.color_stdev = None
        self.black_color = None
        self.is_black_and_white = False
        self.black_point_preset = blackref_preset

    def copy_into(self, source_image, l, t, r, b, target_image, x, y):
        with Image(source_image) as source_image_copy:
            source_image_copy.crop(l, t, r, b)
            target_image.composite_channel(
                "default_channels",
                source_image_copy,
                "over",
                x,
                y,
            )
            target_image.merge_layers("flatten")
        return target_image

    def move_kernel(self, image_size, source_image, l, t, r, b, target_image, x, y):
        if y >= image_size:
            raise ValueError

        target_image = self.copy_into(source_image, l, t, r, b, target_image, x, y)

        if x >= (image_size - self.border_size):
            y += self.border_size
            x = 0
        else:
            x += self.border_size

        return l, t, r, b, target_image, x, y

    def create_black_reference(self):
        with Image(filename=self.negative, resolution=300) as negative_image_container:
            with Image(negative_image_container.sequence[0]) as negative_image:
                use_sides_count = 0
                if self.use_left_border:
                    use_sides_count += 1
                if self.use_right_border:
                    use_sides_count += 1

                use_topbot_count = 0
                if self.use_top_border:
                    use_topbot_count += 1
                if self.use_bottom_border:
                    use_topbot_count += 1

                w, h = negative_image.size
                square_count = (math.floor(w / self.border_size) * use_topbot_count) + (
                    (math.floor(h / self.border_size) - 2) * use_sides_count
                )
                image_size = int(math.sqrt(square_count)) * self.border_size

                with Image(width=image_size, height=image_size) as new_image:
                    negative_image_left = 0
                    negative_image_top = 0
                    negative_image_right = negative_image_left + self.border_size
                    negative_image_bottom = negative_image_top + self.border_size
                    new_image_col = 0
                    new_image_row = 0

                    if self.use_top_border:
                        for idx in range(0, (w - self.border_size), self.border_size):
                            negative_image_left = idx
                            negative_image_top = 0
                            negative_image_right = (
                                negative_image_left + self.border_size
                            )
                            negative_image_bottom = (
                                negative_image_top + self.border_size
                            )
                            try:
                                (
                                    negative_image_left,
                                    negative_image_top,
                                    negative_image_right,
                                    negative_image_bottom,
                                    new_image,
                                    new_image_col,
                                    new_image_row,
                                ) = self.move_kernel(
                                    image_size,
                                    negative_image,
                                    negative_image_left,
                                    negative_image_top,
                                    negative_image_right,
                                    negative_image_bottom,
                                    new_image,
                                    new_image_col,
                                    new_image_row,
                                )
                            except ValueError:
                                break

                    if self.use_left_border:
                        for idx in range(
                            self.border_size, (h - self.border_size), self.border_size
                        ):
                            negative_image_left = 0
                            negative_image_top = idx
                            negative_image_right = (
                                negative_image_left + self.border_size
                            )
                            negative_image_bottom = (
                                negative_image_top + self.border_size
                            )
                            try:
                                (
                                    negative_image_left,
                                    negative_image_top,
                                    negative_image_right,
                                    negative_image_bottom,
                                    new_image,
                                    new_image_col,
                                    new_image_row,
                                ) = self.move_kernel(
                                    image_size,
                                    negative_image,
                                    negative_image_left,
                                    negative_image_top,
                                    negative_image_right,
                                    negative_image_bottom,
                                    new_image,
                                    new_image_col,
                                    new_image_row,
                                )
                            except ValueError:
                                break

                    if self.use_right_border:
                        for idx in range(
                            self.border_size, (h - self.border_size), self.border_size
                        ):
                            negative_image_left = w - self.border_size
                            negative_image_top = idx
                            negative_image_right = (
                                negative_image_left + self.border_size
                            )
                            negative_image_bottom = (
                                negative_image_top + self.border_size
                            )
                            try:
                                (
                                    negative_image_left,
                                    negative_image_top,
                                    negative_image_right,
                                    negative_image_bottom,
                                    new_image,
                                    new_image_col,
                                    new_image_row,
                                ) = self.move_kernel(
                                    image_size,
                                    negative_image,
                                    negative_image_left,
                                    negative_image_top,
                                    negative_image_right,
                                    negative_image_bottom,
                                    new_image,
                                    new_image_col,
                                    new_image_row,
                                )
                            except ValueError as e:
                                break

                    if self.use_bottom_border:
                        for idx in range(0, w, self.border_size):
                            negative_image_left = idx
                            negative_image_top = h - self.border_size
                            negative_image_right = (
                                negative_image_left + self.border_size
                            )
                            negative_image_bottom = (
                                negative_image_top + self.border_size
                            )
                            try:
                                (
                                    negative_image_left,
                                    negative_image_top,
                                    negative_image_right,
                                    negative_image_bottom,
                                    new_image,
                                    new_image_col,
                                    new_image_row,
                                ) = self.move_kernel(
                                    image_size,
                                    negative_image,
                                    negative_image_left,
                                    negative_image_top,
                                    negative_image_right,
                                    negative_image_bottom,
                                    new_image,
                                    new_image_col,
                                    new_image_row,
                                )
                            except ValueError:
                                break

                    new_image.save(filename=self.temp_blackref_image)
                    return self.temp_blackref_image

    def calculate_gamma_correction(self, blackref_image):
        img_minima, img_maxima = blackref_image.range_channel(self.image_channel)
        img_maxima = img_maxima / blackref_image.quantum_range
        img_mean, img_stdev = blackref_image.mean_channel(self.image_channel)
        exposure_mid = img_mean / (blackref_image.quantum_range * 2)
        exposure_gamma_correction = math.log(img_maxima - exposure_mid) / math.log(
            exposure_mid
        )

        if img_maxima >= 1:
            logging.warning("Negative seems to be overexposed")

        return exposure_gamma_correction

    def calculate_shift(self, blackref_image, channel):
        img_minima, img_maxima = blackref_image.range_channel(channel)
        return img_minima

    def calculate_rgb_shifts(self, blackref_image):
        blackref_image.gamma(self.exposure_gamma_correction)
        blackref_image.negate()

        r_shift = self.calculate_shift(blackref_image, "red")
        g_shift = self.calculate_shift(blackref_image, "green")
        b_shift = self.calculate_shift(blackref_image, "blue")

        return r_shift, g_shift, b_shift

    def check_black_and_white(self, blackref_image):
        if blackref_image.colorspace == "gray":
            return True

        if self.bw_autodetect_off:
            return False

        with Image(blackref_image) as blackref_image_copy:
            blackref_image_copy.resize(1, 1)
            color = blackref_image_copy[0, 0]

        self.color_stdev = statistics.stdev(
            [
                color.red / (color.red + color.green + color.blue),
                color.green / (color.red + color.green + color.blue),
                color.blue / (color.red + color.green + color.blue),
            ]
        )

        if self.color_stdev < 0.05:
            return True

        return False

    def analyze_black_reference(self):
        with Image(filename=self.blackref) as blackref_image:
            if blackref_image.colorspace not in ["srgb", "gray"]:
                logging.warning(
                    f" Colorspace '{blackref_image.colorspace}' is neither srgb nor gray"
                )

            self.is_black_and_white = self.check_black_and_white(blackref_image)

            if not self.is_black_and_white:
                # set any black or white pixels to transparent
                with nested(Color("white"), Color("transparent")) as (target, fill):
                    library.MagickOpaquePaintImage(
                        blackref_image.wand,
                        target.resource,
                        fill.resource,
                        blackref_image.quantum_range * self.clipping_fuzz_white,
                        False,
                    )
                with nested(Color("black"), Color("transparent")) as (target, fill):
                    library.MagickOpaquePaintImage(
                        blackref_image.wand,
                        target.resource,
                        fill.resource,
                        blackref_image.quantum_range * self.clipping_fuzz_black,
                        False,
                    )

            # average the colors
            blackref_image.resize(1, 1)
            # remove transparency caused by hiding black and white pixels
            blackref_image.evaluate(
                operator="set", value=int(65535 * 1.0), channel="alpha"
            )

            self.black_color = blackref_image[0, 0]

            self.exposure_gamma_correction = self.calculate_gamma_correction(
                blackref_image
            )
            self.r_shift, self.g_shift, self.b_shift = self.calculate_rgb_shifts(
                blackref_image
            )

            if self.is_black_and_white:
                # shifting color channels for a black and white image
                # makes no sense and in fact produces poor results
                self.shift_color_channels = False

        if not self.save_blackref:
            os.remove(self.blackref)

    def calculate_black_point(self, spinner):
        if (
            self.black_point_preset is not None
            and self.black_point_preset in BLACK_POINT_PRESETS
        ):
            logging.info(f"Using preset black point {self.black_point_preset}")
            self.exposure_gamma_correction = BLACK_POINT_PRESETS[
                self.black_point_preset
            ]["exposure_gamma_correction"]
            self.r_shift = BLACK_POINT_PRESETS[self.black_point_preset]["r_shift"]
            self.g_shift = BLACK_POINT_PRESETS[self.black_point_preset]["g_shift"]
            self.b_shift = BLACK_POINT_PRESETS[self.black_point_preset]["b_shift"]
            self.is_black_and_white = BLACK_POINT_PRESETS[self.black_point_preset][
                "is_black_and_white"
            ]
            self.shift_color_channels = BLACK_POINT_PRESETS[self.black_point_preset][
                "shift_color_channels"
            ]
        else:
            if self.blackref is None:

                sides_used = []
                if self.use_left_border:
                    sides_used.append("left")
                if self.use_right_border:
                    sides_used.append("right")
                if self.use_top_border:
                    sides_used.append("top")
                if self.use_bottom_border:
                    sides_used.append("bottom")
                using_sides = ", ".join(sides_used)
                logging.info(f"  Using sides {using_sides}")

                spinner.start("Creating black point reference")
                self.blackref = self.create_black_reference()
                spinner.succeed("Black point reference created")

            spinner.start("Analyzing black point reference")
            self.analyze_black_reference()
            spinner.succeed("Black point analysis complete")

        logging.info(f" · black color               {self.black_color}")
        logging.info(f"   · red                     {self.black_color.red}")
        logging.info(f"   · green                   {self.black_color.green}")
        logging.info(f"   · blue                    {self.black_color.blue}")
        logging.info(f"   · std.dev                 {self.color_stdev}")
        logging.info(f" · exposure gamma correction {self.exposure_gamma_correction}")
        logging.info(f" · red shift                 {self.r_shift}")
        logging.info(f" · green shift               {self.g_shift}")
        logging.info(f" · blue shift                {self.b_shift}")
        logging.info(f" · black and white           {self.is_black_and_white}")
        logging.info(f" · shift color channels      {self.shift_color_channels}")

    def calculate_color_gammas(self, negative_image):
        with Image(negative_image) as negative_image_copy:
            negative_image_copy.resize(1, 1)

            img_minima_r, img_maxima_r = negative_image_copy.range_channel("red")
            img_minima_g, img_maxima_g = negative_image_copy.range_channel("green")
            img_minima_b, img_maxima_b = negative_image_copy.range_channel("blue")
            img_maxima_r = img_maxima_r / negative_image_copy.quantum_range
            img_maxima_g = img_maxima_g / negative_image_copy.quantum_range
            img_maxima_b = img_maxima_b / negative_image_copy.quantum_range

        gamma_g = 0
        if img_maxima_g > 0:
            gamma_g = math.log(1 / img_maxima_g) / math.log(1 / img_maxima_r)

        gamma_b = 0
        if img_maxima_b > 0:
            gamma_b = math.log(1 / img_maxima_b) / math.log(1 / img_maxima_r)

        return gamma_g, gamma_b

    def calculate_color_factors(self, negative_image):
        with Image(negative_image) as negative_image_copy:
            negative_image_copy.resize(1, 1)

            img_minima_r, img_maxima_r = negative_image_copy.range_channel("red")
            img_minima_g, img_maxima_g = negative_image_copy.range_channel("green")
            img_minima_b, img_maxima_b = negative_image_copy.range_channel("blue")
            img_maxima_r = img_maxima_r / negative_image_copy.quantum_range
            img_maxima_g = img_maxima_g / negative_image_copy.quantum_range
            img_maxima_b = img_maxima_b / negative_image_copy.quantum_range

        factor_g = 0
        if img_maxima_g > 0:
            factor_g = math.log(img_maxima_g) / math.log(img_maxima_r)

        factor_b = 0
        if img_maxima_b > 0:
            factor_b = math.log(img_maxima_b) / math.log(img_maxima_r)

        return factor_g, factor_b

    def adjust_and_save_negative(self):
        with Image(filename=self.negative, resolution=300) as negative_image_container:
            with Image(negative_image_container.sequence[0]) as negative_image:

                if not self.is_black_and_white:
                    # remove black and white pixels
                    # for color negatives, these are scanning artifacts
                    with nested(Color("white"), self.black_color) as (target, fill):
                        library.MagickOpaquePaintImage(
                            negative_image.wand,
                            target.resource,
                            fill.resource,
                            negative_image.quantum_range * self.clipping_fuzz_white,
                            False,
                        )
                    with nested(Color("black"), self.black_color) as (target, fill):
                        library.MagickOpaquePaintImage(
                            negative_image.wand,
                            target.resource,
                            fill.resource,
                            negative_image.quantum_range * self.clipping_fuzz_black,
                            False,
                        )

                negative_image.gamma(self.exposure_gamma_correction)
                negative_image.negate()
                if self.shift_color_channels:
                    negative_image.evaluate(
                        operator="subtract", value=self.r_shift, channel="red"
                    )
                negative_image.normalize(channel="red")
                if self.shift_color_channels:
                    negative_image.evaluate(
                        operator="subtract", value=self.g_shift, channel="green"
                    )
                negative_image.normalize(channel="green")
                if self.shift_color_channels:
                    negative_image.evaluate(
                        operator="subtract", value=self.b_shift, channel="blue"
                    )
                negative_image.normalize(channel="blue")
                negative_image.evaluate(operator="multiply", value=0.99)
                negative_image.evaluate(operator="add", value=100)

                gamma_g, gamma_b = self.calculate_color_gammas(negative_image)
                negative_image.gamma(gamma_g, channel="green")
                negative_image.gamma(gamma_b, channel="blue")

                negative_image.gamma(self.contrast)
                negative_image.negate()
                negative_image.gamma(self.contrast)
                negative_image.negate()

                factor_g, factor_b = self.calculate_color_factors(negative_image)
                negative_image.gamma(factor_g, channel="green")
                negative_image.gamma(factor_b, channel="blue")

                img_minima, img_maxima = negative_image.range_channel(
                    self.image_channel
                )
                img_mean, img_stdev = negative_image.mean_channel(self.image_channel)
                final_gamma = math.log(img_maxima) / math.log(img_mean)
                negative_image.gamma(final_gamma)

                if self.save_flip:
                    negative_image.flip()

                if self.save_flop:
                    negative_image.flop()

                if self.is_black_and_white:
                    negative_image.type = "grayscale"

                if self.save_jpeg:
                    negative_image.format = "jpeg"
                    negative_image.compression_quality = 100

                negative_image.save(filename=self.positive)

    def invert(self):
        if os.path.isfile(self.negative):
            try:
                spinner = Halo(spinner="dots")
                self.calculate_black_point(spinner)
                spinner.start("Adjusting negative")
                self.adjust_and_save_negative()
                spinner.succeed("Positive saved")
            except Exception as e:
                logging.error(f" ERROR: {e}")
        else:
            logging.error(f"File does not exist: {self.negative}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Convert image of a film negative to positive\n\n"
        + "  When automatically generating the black reference,\n"
        + "  it is assumed that the negative is surrounded by a\n"
        + "  narrow strip of unexposed film without sprocket holes,\n"
        + "  so the negative should be cropped to look like this:\n"
        + "\n"
        + "    +-----------------------------+\n"
        + "    | frame border                |\n"
        + "    |    +-------------------+    |\n"
        + "    |    |          /\_      |    |\n"
        + "    |    |      _/\/   \     |    |\n"
        + "    |    |   __/   \_   \/\  |    |\n"
        + "    |    |__/        \__/  \ |    |\n"
        + "    |    | negative image   \|    |\n"
        + "    |    +-------------------+    |\n"
        + "    |                             |\n"
        + "    +-----------------------------+\n"
        + "\n"
        + "  For certain negative types and/or scanning techniques,\n"
        + "  exposing too much of the negative border or sprocket\n"
        + "  holes can cause problems with the automatic adjustment\n"
        + "  of the image. This script automatically adjusts exposure.\n"
        + "  Excessive black pixels in the border region changes the\n"
        + "  historgam,which can prevent setting proper exposure for\n"
        + "  the actualframe of the image. Similar can happen with\n"
        + "  the blank area of the sprocket holes.",
        formatter_class=RawTextHelpFormatter,
    )
    parser.add_argument("negative", metavar="negative", help="negative image file")
    parser.add_argument("positive", metavar="positive", help="positive image file")
    parser.add_argument(
        "--preset",
        dest="black_reference_preset",
        default=None,
        help="use preset black reference information, options are: \n"
        + "\n".join([f" - {k}" for k in BLACK_POINT_PRESETS.keys()]),
    )
    parser.add_argument(
        "--blackref",
        dest="black_reference_image",
        default=None,
        help="use black reference image instead of the frame border,\n"
        + "useful if the frame is not completely surrounded by an\n"
        + "empty border (when there are sprocket holes or with\n"
        + "the first frame of the roll)",
    )
    parser.add_argument(
        "--border-size",
        dest="border_size",
        type=int,
        default=13,
        help="size of frame border, default = 13\n"
        + "(when automatically generating black reference image)",
    )
    parser.add_argument(
        "--ignore-border-left",
        dest="ignore_border_left",
        action="store_true",
        help="ignore the left border when generating black reference",
    )
    parser.add_argument(
        "--ignore-border-right",
        dest="ignore_border_right",
        action="store_true",
        help="ignore the right border when generating black reference",
    )
    parser.add_argument(
        "--ignore-border-top",
        dest="ignore_border_top",
        action="store_true",
        help="ignore the top border when generating black reference",
    )
    parser.add_argument(
        "--ignore-border-bottom",
        dest="ignore_border_bottom",
        action="store_true",
        help="ignore the bottom border when generating black reference",
    )
    parser.add_argument(
        "--contrast",
        dest="contrast",
        type=float,
        default=0.75,
        help="final contrast adjustment, default = 0.75\n",
    )
    parser.add_argument(
        "--clipping-fuzz-black",
        dest="clipping_fuzz_black",
        type=float,
        default=0.01,
        help="fuzziness of the clipping for black, default = 0.01\n"
        + "used when removing frame border and sprocket holes from\n"
        + "color correction calculations (only for color images)",
    )
    parser.add_argument(
        "--clipping-fuzz-white",
        dest="clipping_fuzz_white",
        type=float,
        default=0.01,
        help="fuzziness of the clipping for white, default = 0.01\n"
        + "used when removing frame border and sprocket holes from\n"
        + "color correction calculations (only for color images)",
    )
    parser.add_argument(
        "--jpeg",
        dest="save_jpeg",
        action="store_true",
        help="force JPEG output, when input is not JPEG\n"
        + "also force quality to be 100%%, rather than same as input\n"
        + "(positive image file extension will be set to jpg)",
    )
    parser.add_argument(
        "--flip",
        dest="save_flip",
        action="store_true",
        help="flip final image vertically",
    )
    parser.add_argument(
        "--flop",
        dest="save_flop",
        action="store_true",
        help="flip final image horizontally",
    )
    parser.add_argument(
        "--shift-color-channels",
        dest="shift_color_channels",
        action="store_true",
        help="shift colors by channel to balance them\n",
    )
    parser.add_argument(
        "--bw-autodetect-off",
        dest="bw_autodetect_off",
        action="store_true",
        help="do not infer when color images should be black and white\n"
        + "this is needed when color negatives have grey frame borders\n"
        + "caused by digitizing the negative with a custome white\n"
        + "balance setting",
    )
    parser.add_argument(
        "--save-blackref",
        dest="save_blackref",
        action="store_true",
        help="do not remove generated black reference image swatch\n"
        + "(when automatically generating black reference image)",
    )
    parser.add_argument(
        "-v", "--verbose", dest="verbose", action="store_true", help="verbose output"
    )
    args = parser.parse_args()

    save_blackref = args.save_blackref
    # don't delete user supplied blackref images
    if args.black_reference_image is not None:
        save_blackref = True

    if args.negative and args.positive:
        film = Film(
            args.negative,
            args.positive,
            args.black_reference_preset,
            args.black_reference_image,
            save_blackref,
            args.border_size,
            args.ignore_border_left,
            args.ignore_border_right,
            args.ignore_border_top,
            args.ignore_border_bottom,
            args.contrast,
            args.clipping_fuzz_black,
            args.clipping_fuzz_white,
            args.save_jpeg,
            args.save_flip,
            args.save_flop,
            args.shift_color_channels,
            args.bw_autodetect_off,
            args.verbose,
        )

        signal.signal(signal.SIGINT, signal_handler)
        film.invert()
    else:
        parser.print_usage()
