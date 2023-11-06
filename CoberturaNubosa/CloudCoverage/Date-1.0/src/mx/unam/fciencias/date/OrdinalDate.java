/* -------------------------------------------------------------------
 * OrdinalDate.java
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

package mx.unam.fciencias.date;

/**
 * This class provides the sedrvices required to translate the
 * ordinary date format dd/mm/yyyy to the ordinal one: yyyy-ddd. The
 * days are numbered from 1 (january 1) to 366 (in leap years, usually
 * 365). 
 *
 * @since 1.0
 * @author José Galaviz <jgc@fciencias.unam.mx>
 * @version 1.0
 */

public class OrdinalDate {

    public static final String ERRMSG1 = "Year must be > 1582";
    public static final String ERRMSG2 = 
        "Year > 1582, 1 <= month <= 12, 1 <= day <= corresponding";

    public static final int JANUARY   = 1;
    public static final int FEBRUARY  = 2;
    public static final int MARCH     = 3;
    public static final int APRIL     = 4;
    public static final int MAY       = 5;
    public static final int JUNE      = 6;
    public static final int JULY      = 7;
    public static final int AUGUST    = 8;
    public static final int SEPTEMBER = 9;
    public static final int OCTOBER   = 10;
    public static final int NOVEMBER  = 11;
    public static final int DECEMBER  = 12;

    public static final int MONTHS    = 12;

    public static final int GREGYEAR  = 1582;

    public static final int DAYSPERWEEK = 7;
    
    public static final int SUNDAY    = 0;
    public static final int MONDAY    = 1;
    public static final int TUESDAY   = 2;
    public static final int WEDNESDAY = 3;
    public static final int THURSDAY  = 4;
    public static final int FRIDAY    = 5;
    public static final int SATURDAY  = 6;
    public static final String DAYNAME[] = {"Sunday", 
                                            "Monday", "Tuesday", "Wednesday",
                                            "Thursday", "Friday", "Saturday"};

    public static final int[] DAYSINMONTH = 
       {31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31};

    /**
     * Determines if a given date is correct. year > 1582, 1 <= month
     * <= 12 and day in the range that corresponds to the month.
     * @param year is the year number. It must be > 1582.
     * @param month must be >= 1 and less than or equal to 12.
     * @param day must be in range according to the month.
     * @return true if tha given date is valid, false otherwise.
     */
    private static boolean isValidDate(int year, int month, int day) {
        if ((year > GREGYEAR) && (JANUARY <= month) && (month <= DECEMBER)) {
            if ((month == FEBRUARY) && isLeapYear(year)) {
                return ((0 < day) && (day <= DAYSINMONTH[FEBRUARY - 1] + 1));
            }
            else {
                return ((0 < day) && (day <= DAYSINMONTH[month - 1]));
            }
        }
        else {
            return false;
        }
    }

    /**
     * Returns the number of leap years between the given year and
     * 1582.
     * @param year the year whose previous leap years are requested.
     * @return the number of leap years greater than 1582 and less
     * than the given year.
     * @throws IllegalArgumentException if the given year is less than
     * or equal to 1582.
     */
    public static int leapYears(int year) 
        throws IllegalArgumentException {
        if (year > GREGYEAR) {
            int centenarios, mul400, bisiestos;
            int res400, res100, res4;

            res400 = GREGYEAR - ((GREGYEAR % 400) - 1);
            res100 = GREGYEAR - ((GREGYEAR % 100) - 1);
            res4   = GREGYEAR - ((GREGYEAR % 4)   - 1);
   
            // número de años bisiestos de acuerdo al calendario juliano
            bisiestos = (year - res4) / 4;
            // años centenarios (múltiplos de 100, que no son bisiestos aunque
            // sean múltiplos de 4
            centenarios = (year - res100) / 100;
            bisiestos -= centenarios; // corrección
            // años múltiplos de 400, que a pesar de ser centenarios, son
            // también bisiestos 
            mul400 = (year - res400) / 400;
            bisiestos += mul400; // corrección
            return bisiestos;
        }
        else {
            throw new IllegalArgumentException("OrdinalDate.leapYears" +
                                               ERRMSG1);
        }
    }

    /**
     * This method gives the index of the day of the week that
     * corresponds to the January 1 of the given year.
     * @param year is the number of the year
     * @return an index between 0 (Sunday) and 6 (Saturday) that
     * represents the day of the week by January 1 of the year given
     * as parameter.
     */
    private static int idxDayJan1(int year) {
        return ((4 + (year - GREGYEAR) + leapYears(year)) % DAYSPERWEEK);
    }

    /**
     * Returns the name of the day of the week that corresponds to the
     * January 1 of the given year.
     * @param year is the number of the year (greater than 1582).
     * @return a String with the name of the day of the week that
     * corresponds to January 1 of the year given as paramater.
     * @throws IllegalArgumentExeption if the year is less than or
     * equal to 1582.
     */
    public static String weekDayJan1(int year) 
        throws IllegalArgumentException {
        if (year > GREGYEAR) {
            // el 1o de enero de 1582 fue viernes
            // se avanza un día por año y dos los bisiestos
            return DAYNAME[idxDayJan1(year)];
        }
        else {
            throw new IllegalArgumentException("OrdinalDate.weakDayJan1" +
                                               ERRMSG1);
        }        
    }

    /**
     * This method gives the index of the day of the week that
     * corresponds to the 1st day of the given month of the given
     * year. 
     * @param year is the number of the year
     * @param month is the number of the month
     * @return an index between 0 (Sunday) and 6 (Saturday) that
     * represents the day of the week by the 1st day of the month of
     * the year given as parameter.
     */
    private static int idxDayMon1(int year, int month) {
        int primerdia, i;
        primerdia = idxDayJan1(year);
        for (i = 1; i < month; i++) {
            primerdia += DAYSINMONTH[i - 1];
        }
        if ((month > FEBRUARY) && isLeapYear(year)) {
            primerdia++;
        }
        return primerdia % DAYSPERWEEK;
    }

    /**
     * Returns the name of the day of the week that corresponds to the
     * 1st day of the given month  of the given year.
     * @param year is the number of the year (greater than 1582).
     * @param month is the number of the required month
     * @return a String with the name of the day of the week that
     * corresponds to 1st day of the given month of the year given as
     * paramater. 
     * @throws IllegalArgumentExeption if the year is less than or
     * equal to 1582.
     */
    public static String  weekDayMon1(int year, int month) 
        throws IllegalArgumentException {
        if (isValidDate(year, month, 1)) {
            return DAYNAME[idxDayMon1(year, month)];
        }
        else {
            throw new IllegalArgumentException("OrdinalDate.weakDayMon1" +
                                               ERRMSG2);
        }
    }

    /**
     * This method gives the index of the day of the week that
     * corresponds to the date given.
     * @param year is the number of the year
     * @param month is the number of the month
     * @param day is the number of day
     * @return an index between 0 (Sunday) and 6 (Saturday) that
     * represents the day of the week required
     */
    private static int idxDay(int year, int month, int day) {
        return (idxDayMon1(year, month) + day) % DAYSPERWEEK;
    }

    /**
     * Returns the name of the day of the week that corresponds to the
     * given date.
     * @param year is the number of the year (greater than 1582).
     * @param month is the number of the required month
     * @param day is the number of the day required
     * @return a String with the name of the day of the week that
     * corresponds to the given date
     * @throws IllegalArgumentExeption if the year is less than or
     * equal to 1582.
     */
    public static String weekDay(int year, int month, int day) 
        throws IllegalArgumentException {
        if (isValidDate(year, month, day)) {
            return DAYNAME[idxDay(year, month, day)];
        }
        else {
            throw new IllegalArgumentException("OrdinalDate.weakDay" +
                                               ERRMSG2);
        }
    }

    /**
     * This method determines if a given year is a leap year according
     * to the rules of the Gregorian reform: Evey year which is
     * multiple of 4 is a leap year unless it is also mutiple of 100,
     * in whose case the year is leap if it is also multiple of 400.
     * @param year is the numeric especification of the year. The
     * parameter must be greater then 1582, in which the Gregorian
     * reform was formulated.
     * @return true if the given year is a leap year, false otherwise.
     * @throws IllegalArgumentException if the given year is below
     * 1582.
     */ 
    public static boolean isLeapYear(int year) 
    throws IllegalArgumentException {
        if (year > GREGYEAR) {
            if ((year % 100) == 0) { // if centenial year
                return ((year % 400) == 0); // and multiple of 400
            }
            return ((year % 4) == 0);
        }
        else {
            throw new IllegalArgumentException("OrdinalDate.isLeapYear: " + 
                                               ERRMSG1);
        }
    }

    /**
     * Returns the number of day of the year that corresponds to the
     * given date.
     * @param year is the year of the date. It must be greater than
     * 1582.
     * @param month is a number between 1 and 12 denoting the month of
     * the year.
     * @param day is a number between 1 and the maximum number of days for
     * the given month in the given year.
     * @return the number of days previous and including the given
     * date.
     * @throws IllegalArgumentException if the given date is invalid.
     */
    public static int ordinalDay(int year, int month, int day) 
    throws IllegalArgumentException {
        if (isValidDate(year, month, day)) {
            int prev = 0;
            int i;
            for (i = 0; i < month - 1; i++) {
                prev += DAYSINMONTH[i];
            }
            if (isLeapYear(year) && (month > FEBRUARY)) {
                prev++;
            }
            return prev + day;
        }
        else {
            throw new IllegalArgumentException("OrdinalDate.ordinalDay: " + 
                                               ERRMSG2);
        }
    }

    public static float timeFrac(int hour, int mins) {
        return (float)hour + (float)mins/60;
    }

    /**
     * Main program. An example.
     */
    public static void main(String args[]) {
        int anno = 2100;
        int dia = 1;
        int mes = 1;

        for (mes = 1; mes <= 12; mes++) {
            for (dia = 1; dia <= 31; dia++) {
                System.out.print(" " + dia + " / " + mes + " / " + anno + " ");
                if (isValidDate(anno, mes, dia)) {
                        System.out.print("= " + ordinalDay(anno, mes, dia));
                        System.out.println(" -> " + weekDay(anno, mes, dia));
                }
                else {
                    System.out.println(" Fecha inválida");
                }
            }
        }
        int horas = 23;
        int minutos = 30;
        System.out.println("Time: " + horas + ":" + minutos+ " = " +
                           timeFrac(horas, minutos));
    }

} // OrdinalDate.java ends here.
