/* -------------------------------------------------------------------
 * Filter.java
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
 * Defines the services associated with the methods to distinguish
 * clouds and sky. 
 *
 * @since 1.0
 * @author José Galaviz <jgc@fciencias.unam.mx>
 * @version 1.0 &nbsp; june 2009
 */
public interface Filter {
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
    public BufferedImage filtering(BufferedImage imgsrc);
} // Filter.java ends here.
