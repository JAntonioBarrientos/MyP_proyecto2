/* -------------------------------------------------------------------
 * Cleaner.java
 * version 1.0
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
 * This class provides the services needed to crop the whole image
 * to obtain the square where the actual sky picture is. The sky
 * picture is the incircle.
 *
 * @since 1.0
 * @author José Galaviz <jgc@fciencias.unam.mx>
 * @version 1.0 &nbsp; june 2009
 */

public class Cleaner {
    private BufferedImage msk;
    private int side;
    private double radius;

    /**
     * Builds an instance of Cleaner based on an image mask. Such mask
     * must be a white circle inscribed in a square. The circle must
     * mask the picture in an image, the black exterior of the circle
     * must mask the boundary of the picture, which must be ignored by
     * the image processing algorithms.
     * @param filemask is a String with the name of the file which
     * defines the mask.
     */
    public Cleaner(String filemask)
      throws IOException {
      msk  = ImageIO.read(new File(filemask));
      side = msk.getWidth();
      radius = (double) side / 2.0;
    }

    /**
     * Method for crop the picture area of a BufferedImage.
     * @param img is the BufferedImage to be masked by the
     * Cleaner.
     * @return a new BufferedImage, a square which contains only the
     * picture in the parameter, surrounded by a black area.
     */
    public BufferedImage crop(BufferedImage img) {
        // 4BYTE_ABGR means 1 byte for R, 1 for G, 1 for B and 
        // 1 for the alpha chanel
        BufferedImage res = new BufferedImage(side, side, 
                                              BufferedImage.TYPE_4BYTE_ABGR);
        int  i, j, initi, initj;
        int  mskcolor;
        int  nren = img.getHeight();
        int  ncol = img.getWidth();
        initi = (nren - side) / 2;
        initj = (ncol - side) / 2;
        /*
           left margin (no picture) -> {0, 1, ..., initi - 1}
           picture square -> {initi, initi + 1, ..., initi + side - 1}
           right margin (no picture)  -> {initi + side, ..., 2*initi + side -1}
           for each pixel in the region delimited by the mask...
        */
        for (i = 0; i < side; i++) {
            for (j = 0; j < side; j++) {
                /* set the alpha chanel to 0XFF, the RGB chanels are set to the
                   result obtained by the AND of the value in the image and the
                   mask since the mask is white (0XFF) in the picture region,
                   and black (0X00) otherwise, the resulting image is a perfect
                   circle with the picture surrounded by a black boundaries.
                */
                mskcolor = msk.getRGB(j, i);
                // outside picture, where the mask is black
                if ((mskcolor & 0X00FFFFFF) == 0) { 
                    res.setRGB(j, i, 0X00000000); // set black but transparent
                }
                else { // sky picture set alpha to opaque OR 
                    // the pixel AND the mask (which is white)
                    res.setRGB(j, i, (0XFF000000) | 
                                       (img.getRGB(j + initj, i + initi) &
                                        mskcolor));
                }
            }
        }
        return res;
    }
} // Cleaner.java ends here.
