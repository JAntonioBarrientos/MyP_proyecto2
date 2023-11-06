/*
  schedule.c
*/
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>

/**
 * Este programa determina todos las fechas de los días de
 * clase que corren tradicionalmente a cargo del
 * profesor o el ayudante de un curso típico del área
 * físico-matemática en la Facultad de Ciencias. 
 *
 * José Galaviz
 * noviembre de 1999
 */

#define GREG     1582

#define ENERO       1
#define FEBRERO     2
#define MARZO       3
#define ABRIL       4
#define MAYO        5
#define JUNIO       6
#define JULIO       7
#define AGOSTO      8
#define SEPTIEMBRE  9
#define OCTUBRE    10
#define NOVIEMBRE  11
#define DICIEMBRE  12

#define DIASXSEMANA 7

#define DOMINGO   0
#define LUNES     1 
#define MARTES    2
#define MIERCOLES 3
#define JUEVES    4
#define VIERNES   5
#define SABADO    6

#define DIASXMES  {0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31}

int dias_mes[13] = DIASXMES;

/*
  En 1582 el papa Gregorio XII llevó a cabo la reforma al calendario
  juliano, dando lugar al gregoriano. 
 */

/*
  Determina el número de años bisiestos transcurridos desde 1582, de
  acuerdo a la reforma gregoriana del calendario. Son bisiestos todos
  los años múltiplos de 4, excluyendo a todos aquellos que sean
  múltiplos de 100 (centenarios), pero incluyendo aquellos que, además
  de ser multiplos de 100 también lo sean de 400.
  Params: anio es un entero mayor a 1582 (año de la reforma
  gregoriana).
  Return: un entero no negativo que indica el número de años bisiestos
  entre 1582 y el año dado como parámetro. Regresa -1 si el parámetro
  es menor a 1582.
 */
int  numBisiestos(int anio);

/*
  Determina el día de la semana en que cayó el 1 de enero del año dado
  como argumento.
  Param: anio es el año del que se quiere saber el día de la semana en
  que cayó el 1 de enero.
  Return: un entero en el conjunto {0, ..., 6} que indica el día de la
  semana en que cayó el 1 de enero del año dado como
  parámetro. Regresa -1 si el año dado es menor a 1582.
 */
int  diaSem1Enero(int anio);

/*
  Determina si un año dado es bibiesto o no.
  Param: anio es el año que se quiere saber si es bisiesto o no.
  Return: Regresa 1 si el año es bisiesto y 0 en otro caso.
 */
int  esBisiesto(int anio);

/*
  Dados un año y un mes, regresa el día de la semana en que cayó el
  primero día de dicho mes en el año indicado.
  Param: anio es el año en cuestión. Debe ser mayor a 1582.
  Param: mes es el número de mes en cuestión {0, ... ,11}
  Return: El día de la semana en que cayó el primer día del mes en el
  año en cuestión {0, ..., 6}. Regresa -1 si el año es menor a 1582 o
  si el mes es negativo o mayor a 11.
 */
int  diaSem1Mes(int anio, int mes);

/*
  Escribe los días del mes que empatan con un criterio establecido.
  Param: mes es el mes que se desea escribir.
  Param: anio es el año al que pertenece el mes que se desea.
  Param: pr establece el criterio de empate. pr = 1 significa que se
  despliegan todas las fechas que correspondan a lunes, miércoles y
  viernes. pr = 0 significa que son los martes y jueves.
  WARNING: Acceso a variables globales de riesgo.
  Se accede implícitamente al arreglo de cadenas, al
  contador global de fechas y al marcador de descanso. Los
  tres se modifican. 
 */
void escribeMes(int mes, int anio, int pr);

/*
  Determina la fecha de inicio la semana santa (en lo laboral). Es
  decir obtene la fecha de lunes siguiente al Domingo de Ramos (una
  semana antes del Domingo de Pascua). El día que tiene definición
  precisa es justamente el domingo de pascua: el domingo inmediato
  siguiente a la luna llena del mes judío de Nissan (22 de marzo al 25
  de abril), es decir el domingo siguiente a la primera luna llena de
  primavera. La definición se promulgó en el concilio de Nicea de
  325. El algoritmo que se utiliza es perpetuo y data de 1876, fue
  publicado en el Butcher's Eclesiastical Calendar.
  Param: anio es el año en que se quiere obtener la fecha del lunes de
  la semana de descanso.
  Param: fecha es un arreglo en el que se almacena la fecha de inicio
  de la semana de descanso fecha[0] contiene el día y fecha[1] el mes
  {0, ..., 6}.
 */
void fecha1SemanaSanta(int anio, int fecha[]);

/*
  Obtiene los valores numéricos de una fecha dada en una
  cadena de texto en el formato dd/mm/aaaa. El año debe ser
  mayor a 1582.
  Param: cad es la cadena donde se encuentra la fecha
  especificada.
  Param: *dd para guardar el día.
  Param: *mm para guardar el mes.
  Param: *aaaa para guardar el año.
  Return: 1 si la fecha pudo ser extraida de la cadena, -1
  en otro caso.
*/
int parseFecha(char* cad, int* dd, int* mm, int* aaaa);

/*
  Marca como dias de inválidos aquellos que están fuera del
  rango especificado y como de asueto los de semana santa y aquellos
  especificados en el archivo "asueto.txt".
  Param: di, mi y ai son respectivamente el día, mes y año
  de la fecha inicial.
  Param df, mf y af son respectivamente el día, mes y año de
  la fecha final.
  Param: pr indica si se trata de días de clase de profesor (1)
  o de ayudante (0).
  WARNING: Acceso a variables globales de riesgo.
  Se accede implícitamente al arreglo de cadenas y al
  contador global de fechas. No se modifican. También se
  accede al arreglo de marcas de dias de descanso, que sí se
  modifica.
 */
void correccionAsueto(int di, int mi, int ai, int df, int mf, int af, int pr);

/*
  Regresa las cadenas de los cinco días de la semana santa.
  Param: anio contiene el año del que se quiere la semana
  santa.
  Param: fechas almacena las cinco cadenas de los días (de
  lunes a viernes) de la semana santa.
*/
void fechasSemanaSanta(int anio, char *fechas[]);

/*
  Busca una fecha específica en el arreglo de cadenas de
  fecha.
  Param: fecha es la cadena a buscar "SS dd/mm/aaaa" SS es
  día de la semana {Lu, Ma, Mi, Ju, Vi}.
  Return: el índice donde la cadena fue encontrada o 0 en
  otro caso.
  WARNING: Acceso a variables globales de riesgo.
  Se accede implícitamente al arreglo de cadenas y al
  contador global de fechas. No se modifican.
 */
int buscaFechaCompleta(char *fecha);

/*
  Busca una fecha específica en el arreglo de cadenas de
  fecha.
  Param: fecha es la cadena a buscar "dd/mm/aaaa".
  Return: el índice donde la cadena fue encontrada o 0 en
  otro caso.
  WARNING: Acceso a variables globales de riesgo.
  Se accede implícitamente al arreglo de cadenas y al
  contador global de fechas. No se modifican.
 */
int buscaFecha(char *fecha);

/*
  Compara dos fechas.
  Param: fecha1 y fecha2 son las fechas a comparar (cadenas
  en formato "dd/mm/aaa" sin día de la semana).
  Return: un número negativo si fecha1 <  fecha2, uno
  positivo si fecha1 >  fecha2, cero si son iguales.
 */
int comparaFechas(char *fecha1, char *fecha2);


int    td, tm, ta;
int    fd, fm, fa;
int    mesi, mesf, mescnt;
int    i, j;
int    prof;

/*
  Variables globales de riesgo
*/
int    *descanso; /* marca los días de descanso */
char*  *cadenas;  /* cadenas de fechas "SS dd/mm/aaaa" */
int    gcount;    /* número real de fechas almacenadas */

char  tema[90][100];


main(int argc, char *argv[])
{
   
   if ((argc != 4) ||
       ((toupper(argv[1][0]) != 'A') &&
        (toupper(argv[1][0]) != 'P')) ||
       (parseFecha(argv[2], &fd, &fm, &fa) < 0) ||
       (parseFecha(argv[3], &td, &tm, &ta) < 0)       
      ) {
      fprintf(stderr, "Uso: %s [a|A|p|P] DD/MM/AAAA DD/MM/AAAA \n", argv[0]);
      fprintf(stderr, "a|A = Dias del ayudante. p|P = Dias del profesor\n");      
      exit(1);
   }
   prof = (toupper(argv[1][0]) == 'P') ? 1 : 0;
   /*
   fprintf(stderr, "Del %d %d %d al %d %d %d\n",
           fd, fm, fa, td, tm, ta);
   */

   gcount = 1; /* variable global */
   
   mesi = fm;
   mesf = DICIEMBRE;
   mescnt = 0;
   for (i = fa; i <= ta; i++) {
      if (i > fa)  mesi = 1;
      if (i == ta) mesf = tm;
      for (j = mesi; j <= mesf; j++) {
         mescnt++;
      }
   }

   mescnt *= 15;
   descanso =  (int *)  malloc(sizeof(int)   * mescnt);
   cadenas  =  (char **)malloc(sizeof(char*) * mescnt);
   
   for (i = 0; i < mescnt; i++){
      cadenas[i] = (char *)malloc(sizeof(char) * 14);
   }

   sprintf(cadenas[0], "Dummy string");
   descanso[0] = 2;
   
   mesi = fm;
   mesf = DICIEMBRE;
   /* Recorriendo los años pedidos */
   for (i = fa; i <= ta; i++) {
      if (i > fa)  mesi = 1;
      if (i == ta) mesf = tm;
      /* Recorriendo los meses pedidos */
      for (j = mesi; j <= mesf; j++) {
         /* WARNING: modifica gcount, descanso y cadenas */
         escribeMes(j, i, prof);
      }
   }

   /* WARNING: modifica descanso */
   correccionAsueto(fd, fm, fa, td, tm, ta, prof);

   /* inicio */
   FILE  *f;
   char  c;
   f = fopen("temas.txt", "r");
   int nls = 1;
   while (!feof(f)) {
      fgets(tema[nls], 100, f);
      for (i = 0; (i < 100) && (tema[nls][i] != '\n'); i++);
      tema[nls][i-1] = '\x0';
      nls++;
      c = fgetc(f);
      if (!feof(f))
         ungetc(c, f);
   }
   fclose(f);
   /* fin   */
   for (i = 1, j = 1; i < gcount; i++) {
      if (descanso[i] != 2) {
         printf("<tr><td align=\"left\">%s</td><td align=\"left\">", cadenas[i]);
         if (descanso[i] == 1)
            printf("<i>Asueto</i></td></tr>");
         else
            printf("%s</td></tr>", tema[j++]);
         printf("\n");
      }
   }
}

void correccionAsueto(int di, int mi, int ai, int df, int mf, int af, int pr)
{
   int  i, j, k;
   char *sesa[5];
   char fechaini[14] = "             \x0";
   char fechafin[14] = "             \x0";

   sprintf(fechaini, "   %2d/%02d/%4d\x0", di, mi, ai);
   sprintf(fechafin, "   %2d/%02d/%4d\x0", df, mf, af);

   /* asueto para ... */
   /* todas las fecha anteriores a la incial */
   for (i = 0; comparaFechas(cadenas[i] + 3, fechaini + 3) < 0; i++)
      descanso[i] = 2;
   /* y las posteriores a la final */
   for (i = gcount - 1; comparaFechas(cadenas[i] + 3, fechafin + 3) > 0; i--)
      descanso[i] = 2;
        
   for (i = 0; i < 5; i++){
      sesa[i] = (char *)malloc(sizeof(char) * 3);
   }

   /* Para todos los años considerados */
   for (i = ai; i <= af; i++) {
      /* asueto en semana santa */
      fechasSemanaSanta(i, sesa);
      for (j = 0; j < 5; j++)
         descanso[buscaFechaCompleta(sesa[j])] = 1;
   }
   /* asuetos basados en archivo */
   FILE  *f;
   char  linea[11] = "          \x0";
   char  c;
   f = fopen("asueto.txt", "r");
   int nls = 0;
   while (!feof(f)) {
      fgets(linea, 15, f);
      for (i = 0; (i < 15) && (linea[i] != '\n'); i++);
      linea[i] = '\x0';
      descanso[buscaFecha(linea)] = 1;
      nls++;
      c = fgetc(f);
      if (!feof(f))
         ungetc(c, f);
   }
   fclose(f);
}

void escribeMes(int mes, int anio, int pr)
{
   int prim, i, j, ndias;
   
   prim  = diaSem1Mes(anio, mes);
   ndias = dias_mes[mes];
   if ((mes == FEBRERO) && (esBisiesto(anio)))
      ndias++;
   
   for (i = 1, j = prim; i <= ndias; i++, j++, j = j % DIASXSEMANA) {
      if (((j == LUNES)     ||
           (j == MIERCOLES) ||
           (j == VIERNES))  &&
          pr) {
         switch (j) {
            case LUNES     : sprintf(cadenas[gcount], "Lu %2d/%02d/%4d\x0", i, mes, anio);
                             break;
            case MIERCOLES : sprintf(cadenas[gcount], "Mi %2d/%02d/%4d\x0", i, mes, anio);
                             break;
            case VIERNES   : sprintf(cadenas[gcount], "Vi %2d/%02d/%4d\x0", i, mes, anio);
         }
         descanso[gcount] = 0;
         gcount++;
      }
      else if (((j == MARTES) ||
                (j == JUEVES)) &&
               !pr) {
         switch (j) {
            case MARTES : sprintf(cadenas[gcount], "Ma %2d/%02d/%4d\x0", i, mes, anio);
                          break;
            case JUEVES : sprintf(cadenas[gcount], "Ju %2d/%02d/%4d\x0", i, mes, anio);
         }
         descanso[gcount] = 0;
         gcount++;
      }
   }
}

int parseFecha(char* cad, int* dd, int* mm, int* aaaa)
{
   char   dia[3];
   char   mes[3];
   char   anio[5];
   
   dia[0]  = *(cad);
   dia[1]  = *(cad + 1);
   dia[2]  = '\0';
   
   mes[0]  = *(cad + 3);
   mes[1]  = *(cad + 4);
   mes[2]  = '\0';
   
   anio[0] = *(cad + 6);
   anio[1] = *(cad + 7);
   anio[2] = *(cad + 8);
   anio[3] = *(cad + 9);
   anio[4] = '\0';
   
   *dd   = atoi(dia);
   *mm   = atoi(mes);
   *aaaa = atoi(anio);
   
   if ((*dd > 0) && (*dd < 32) &&
       (*mm > 0) && (*mm < 13) &&
       (*aaaa > GREG))
      return 1;
   else
      return -1;
}

int  numBisiestos(int anio)
{
   int centenarios, mul400, bisiestos;
   int res400, res100, res4;

   res400 = GREG - ((GREG % 400) - 1);
   res100 = GREG - ((GREG % 100) - 1);
   res4   = GREG - ((GREG % 4)   - 1);
   
   if (anio < GREG) return -1;

   // número de años bisiestos de acuerdo al calendario juliano
   bisiestos = (anio - res4) / 4;
   // años centenarios (múltiplos de 100, que no son bisiestos aunque
   // sean múltiplos de 4
   centenarios = (anio - res100) / 100;
   bisiestos -= centenarios; // corrección
   // años múltiplos de 400, que a pesar de ser centenarios, son
   // también bisiestos 
   mul400 = (anio - res400) / 400;
   bisiestos += mul400; // corrección
   return bisiestos;
}

int  diaSem1Enero(int anio)
{
   if (anio < GREG) return -1;

   // el 1o de enero de 1582 fue viernes
   // se avanza un día por año y dos los bisiestos
   return ((5 + (anio - GREG) + numBisiestos(anio)) % DIASXSEMANA);
}

int  esBisiesto(int anio)
{
   // los múltilos de 100 son bisiestos solo si son también
   // múltiplos de 400 
   if (!(anio % 100)) return ((anio % 400) == 0);

   return ((anio % 4) == 0);
}

int  diaSem1Mes(int anio, int mes)
{
   int primerdia, i;

   if (anio < GREG) return -1;

   if ((mes < ENERO) || (mes > DICIEMBRE)) return -1;

   primerdia = diaSem1Enero(anio);

   for (i = 1; i < mes; i++)
      primerdia += dias_mes[i];

   if ((mes > FEBRERO) && esBisiesto(anio))
      primerdia++;

   return (primerdia % DIASXSEMANA);
}

void fechasSemanaSanta(int anio, char *fechas[])
{
   int  primlunes[2];
   int  dss, mss;
   int  i;
   char dssem[3] = "   ";
   
   fecha1SemanaSanta(anio, primlunes);

   /* primer lunes de descanso */
   dss = primlunes[0];
   mss = primlunes[1];
   sprintf(fechas[0], "Lu %2d/%02d/%4d\x0", dss, mss, anio);
   /* dias siguientes, si llegamos a 31 de marzo, sigue el 1
    * de abril */
   for (i = 1; i < 5; i++) {
      if (dss == 31) {
         mss++;
         dss = 1;
      }
      else
         dss++;
      switch (i) {
         case  1 : sprintf(dssem, "Ma\x0");
                   break;
         case  2 : sprintf(dssem, "Mi\x0");
                   break;
         case  3 : sprintf(dssem, "Ju\x0");
                   break;
         case  4 : sprintf(dssem, "Vi\x0");
      }
      sprintf(fechas[i], "%s %2d/%02d/%4d\x0", dssem, dss, mss, anio);
   }
   /*
   for (i = 0; i < 5; i++) {
      fprintf(stderr, "Santo %s\n", fechas[i]);
   }
   */
}

void fecha1SemanaSanta(int anio, int fecha[])
{
   /*
     Algoritmo de Butcher
    */
   int a, b, c, d, e, f, g;
   int h, i, k, l, m, p;
   int aux;
   int mes, dia;

   a = anio % 19;
   b = anio / 100;
   c = anio % 100;
   d = b / 4;
   e = b % 4;
   f = (b + 8) / 25;
   g = (b - f + 1) / 3;
   h = (19 * a + b - d - g + 15) % 30;
   i = c / 4;
   k = c % 4;
   l = (32 + 2 * e + 2 * i - h - k) % DIASXSEMANA;
   m = (a + 11 * h + 22 * l) / 451;
   aux = h + l - 7 * m + 114;
   mes = aux / 31;
   p = aux % 31;
   dia = p + 1;
   /* dia y mes contienen ahora la fecha del domingo de
    * pascua. Se procede a calcular la fecha del lunes
    * siguiente al domingo de ramos (1er lunes de descanso)
    * */ 
   if (dia < 7) {
      dia = 31 - (6 - dia);
      mes--;
   }
   else {
      dia -= 6;
   }
   fecha[0] = dia;
   fecha[1] = mes;
}

int buscaFechaCompleta(char *fecha)
{
   int i;
   for (i = gcount - 1; (i > 0) && strcmp(fecha, cadenas[i]); i--);
   return i;
}

int buscaFecha(char *fecha)
{
   int i;
   for (i = gcount - 1; (i > 0) && strcmp(fecha, cadenas[i] + 3); i--);
   return i;
}

int comparaFechas(char *fecha1, char *fecha2)
{
   int d1, m1, a1, d2, m2, a2;
   parseFecha(fecha1, &d1, &m1, &a1);
   parseFecha(fecha2, &d2, &m2, &a2);
   if (a1 != a2) return a1 - a2;
   if (m1 != m2) return m1 - m2;
   return d1 - d2;
}
