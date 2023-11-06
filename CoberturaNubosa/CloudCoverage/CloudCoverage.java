/* -------------------------------------------------------------------
 * CloudCoverage.java
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

import java.awt.Image;
import java.awt.image.BufferedImage;
import java.awt.image.RenderedImage;
import java.io.File;
import java.io.IOException;
import javax.imageio.ImageIO;
import mx.unam.fciencias.sky.*;
import mx.unam.fciencias.date.*;

/**
 * Calculates the cloud coverage index from pictures of the sky.
 *
 * @since
 * @author José Galaviz <jgc@fciencias.unam.mx>
 * @version
 */

public class CloudCoverage {

    public static double sunDeclination(int year, int month, int day) 
    throws IllegalArgumentException {
        double diaanno = (double) OrdinalDate.ordinalDay(year, month, day);
        double fact = 360/365;
        return -23.45 * Math.cos(fact * (diaanno + 10));
    }

    public static double trueTime(double longitude, int hour, int min, int tz, boolean dlst) {
        double hora = (double)OrdinalDate.timeFrac(hour, min);
        // tz must be -6
        hora += longitude/15 - (double)tz;
        hora -= dlst ? 1 : 0;
        // falta usar la equation of time, se supone
        return hora;
    }

    public static double hourAngle(double truet) {
        double factor = 2.0 * Math.PI / 360.0;
        return (12.0 - truet) * 15.0 * factor;
    }

    public static double cloudCoverage(BufferedImage img) {
        double ang;
        int    i, j;
        double xcomp, ycomp;
        int    pelcolor;
        int    tam = img.getWidth();
        double radious = (double)tam/2.0;

        double rv, cosa, sena, weight;
        double total, clouds;

        total = clouds = 0.0;
        for (i = 0; i < tam; i++ ){
            for (j = 0; j < tam; j++) {
                pelcolor = img.getRGB(j, i);
                if ((pelcolor & 0XFF000000) == 0XFF000000) { // picture pel
                    xcomp = ((double)j - radious) * ((double)j - radious);
                    ycomp = ((double)i - radious) * ((double)i - radious);
                    rv = Math.sqrt(xcomp + ycomp);
                    rv = rv / radious;
                    if (rv <= 1) {
                        rv = rv * Math.PI/2.0;
                        rv = rv * rv;
                        cosa = Math.cos(0.35 * rv - 0.02);
                        sena = 1.0 + Math.sin(0.176 * rv - 0.0042);
                        weight = cosa * sena;
                        total += weight;
                        if ((pelcolor & 0XFFFFFFFF) == 0XFFFFFFFF) { //cloud
                            clouds += weight;
                        } //cloud pel
                    } // in picture pel (radious)
                } // in picture pel (transp)
            }
        }
        return clouds / total;
    }

    /**
     * Main method for testing the services of Cleaner.
     */
    public static void main(String[] args) {
        String gname;
        String cleanname = "mask-1350-sq.png";
        double ccover;
        try {
            String frmt = "PNG";
            gname = args[0].substring(0, args[0].lastIndexOf("."));

            System.out.println("Reading image file: " + args[0]);
            BufferedImage image = ImageIO.read(new File(args[0]));

            Cleaner lim = new Cleaner(cleanname);
            System.out.println("Cleaning according to: " + cleanname);
            BufferedImage cleanimage = lim.crop(image);
            System.out.println("Writing clean file: " + gname + "-clean.png");
            ImageIO.write(cleanimage, frmt, new File(gname+"-clean.png"));

            RGBFilter filterRB = new RGBFilter(0.95);
            System.out.println("Filtering with R/B criteria");
            BufferedImage filteredimage = filterRB.filtering(cleanimage);
            System.out.println("Writing filtered file: " + gname + "-filter.png");
            ImageIO.write(filteredimage, frmt, new File(gname+"-filter.png"));

            Convolution convol = new Convolution(5, 12);
            System.out.println("Convolving");
            BufferedImage convolutionimage = convol.applyConvolution(filteredimage);
            System.out.println("Writing convolved file: " + gname + "-convolved.png");
            ImageIO.write(convolutionimage, frmt, new File(gname+"-convolved.png"));

            System.out.println("Calculating cloud coverage index (clouds/total)");
            ccover = cloudCoverage(convolutionimage);
            System.out.println("Cloud coverage: " + ccover);
        }
        catch (IOException ioe) {
            System.err.println("I/O Error");
            ioe.printStackTrace(System.err);
            System.exit(1);
        }
    }

} // CloudCoverage.java ends here.
