/* -------------------------------------------------------------------
 * RGBFilter.java
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

import java.lang.IllegalArgumentException;
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
public class RGBFilter implements Filter {

    private static final String ERR_MSG = "ratio must be in [0,1]";

    /**
     * Threshold for the red/blue ratio. Below this value the pixel is
     * sky, cloud otherwise.
     */
    private double threshold;

    /**
     * Builds a new instance of RGBFilter settingthe threshold value
     * for the red/blue ratio.
     * @param rbratio is a number in [0,1] whose value is used to
     * classify the pixels: below the rbratio the pixel is classified
     * as sky, greater or equal values are "sky" pixels.
     * @throws IllegalArgumentException if the parameter is not in the
     * [0, 1] interval.
     */
    public RGBFilter(double rbratio) 
    throws IllegalArgumentException {
        if ((0 <= rbratio) && (rbratio <= 1)) {
            threshold = rbratio;
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
    public BufferedImage filtering(BufferedImage imgsrc) {
        int  i, j, side;
        int  pelcolor;
        double ratio;
        side  = imgsrc.getWidth();
        // 4BYTE_ABGR means 1 byte for R, 1 for G, 1 for B and 
        // 1 for the alpha chanel
        BufferedImage  res = new BufferedImage(side, side, 
                                               BufferedImage.TYPE_4BYTE_ABGR);
        for (i = 0; i < side; i++) {
            for (j = 0; j < side; j++) {
                pelcolor = imgsrc.getRGB(j, i);
                if ((pelcolor & 0X00FFFFFF) == 0) {// outside pict, black pixel
                    res.setRGB(j, i, 0X00000000); // set black but transparent
                }
                else { // inside picture
                    // take the red chanel value
                    ratio = (double)((pelcolor & 0X00FF0000) >> 16);
                    // divide by the blue chanel value
                    ratio = ratio / (double)(pelcolor & 0X000000FF);
                    // if ratio is below the threshold
                    if (ratio < threshold) {
                        // black (but opaque) means sky
                        res.setRGB(j, i, 0XFF000000);
                    }
                    else { // ratio above or equal the threshold
                        // white and opaque means cloud
                        res.setRGB(j, i, 0XFFFFFFFF);
                    }
                } // inside picture
            } // for j
        } // for i
        return res;
    }
} // RGBFilter.java ends here.
