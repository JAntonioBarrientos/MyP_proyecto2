/* -------------------------------------------------------------------
 * Convolution.java
 * version
 * Copyright (C) 2009  José Galaviz Casas,
 * Faculty of Sciences,
 * Universidad Nacional Autónoma de México, Mexico.
 *
 * This program is free software; you can redistribute it and/or
 * modify it under the terms of the GNU General Public License
 * as published by the Free Software Foundation; either version 2
 * of the License, or (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program; if not, visit the following URL:
 * http://www.gnu.org/licenses/gpl.html
 * or write to the Free Software Foundation, Inc.,
 * 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
 * -------------------------------------------------------------------
 */

package mx.unam.fciencias.sky;

import java.awt.Image;
import java.awt.image.BufferedImage;
import java.awt.image.RenderedImage;
import java.io.File;
import java.io.IOException;
import javax.imageio.ImageIO;

/**
 * Defines a filter based on the red/blue ratio for each pixel. The
 * objective is the picture segmentation, which leads to the cloud
 * Vs. sky identification.
 *
 * @since 1.0
 * @author José Galaviz <jgc@fciencias.unam.mx>
 * @version 1.0 &nbsp; june 2009
 */
public class Convolution {

    private static final String ERR_MSG = 
        "neighborhood side must be odd and votes in {1,...,side*side-1}";

    /**
     * Threshold for the voting to be a cloud pel
     */
    int minvotos;
    /**
     * Side of a square neighborhood
     */
    int neighside;

    /**
     * Builds a new instance of Convolution operator.
     * @param side is the size of a neighborhood side in which the
     * central pel must be determined. This parameter must be odd.
     * @param minvoteschange set the minimum number of votes required to
     * change the pel value.
     * @throws IllegalArgumentException if the side is not odd number
     * or votes is not in the set {1, ..., side*side - 1}
     */
    public Convolution(int side, int minvoteschange) 
    throws IllegalArgumentException {
        if ((side % 2 == 1) && 
            (1 <= minvoteschange) && (minvoteschange < side*side)) {
            minvotos = minvoteschange;
            neighside = side;
        }
        else {
            throw new IllegalArgumentException(this.getClass().getName() +
                                               " Constructor: " + ERR_MSG);
        }
    }

    /**
     * Method for to distinguish clouds and sky in a picture.
     * @param imgsrc the source picture. It is a square image whose
     * inscribed circle contains the picture to be analyzed. Outside
     * the circle the image must be entirely black with alpha chanel
     * set to zero (completely transparent). The sky picture in the
     * circle must have alpha chanel set to 0XFF (completely opaque).
     * @return a new B/W image: all the sky pixels must be black and
     * all the cloud pixels must be white. In order to distinguish the
     * sky and background pixels, these last must have alpha cnanel
     * set to zero.
     */
    public BufferedImage applyConvolution(BufferedImage imgsrc) {
        int  i, j, side, nesi = neighside / 2;
        int  pelcolor;
        double ratio;
        side  = imgsrc.getWidth();
        // 4BYTE_ABGR means 1 byte for R, 1 for G, 1 for B and 
        // 1 for the alpha chanel
        BufferedImage  res = new BufferedImage(side, side, 
                                               BufferedImage.TYPE_4BYTE_ABGR);
        for (i = nesi; i < side - nesi; i++) {
            for (j = nesi; j < side - nesi; j++) {
                pelcolor = imgsrc.getRGB(j, i);
                if (pelcolor == 0X00000000) {// outside pict, black pixel
                    res.setRGB(j, i, 0X00000000); // set black but transparent
                }
                else { // inside picture
                    int  n, m, nv;
                    nv = 0;
                    for (n = i - nesi; n <= i + nesi; n++) {
                        for (m = j - nesi; m <= j + nesi; m++) {
                            if ((imgsrc.getRGB(m, n) ^ pelcolor) != 0) {
                                nv++;
                            }
                        }
                    }
                    if (nv >= minvotos) res.setRGB(j, i, 0XFF000000 | ~pelcolor);
                    else res.setRGB(j, i, 0XFF000000 | pelcolor);
                } // inside picture
            } // for j
        } // for i
        return res;
    }
} // Convolution.java ends here.
