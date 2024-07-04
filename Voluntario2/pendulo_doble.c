#include <stdio.h>
#include <math.h>

//// CONSTANTES en el Sitema Internacional
#define g 9.8           // Aceleracion de la gravedad en la Tierra
#define PI 3.14159265358979323846

//// FUNCIONES
double y1dot(double y1, double y2, double y3, double y4){
    return y3;
}

double y2dot(double y1, double y2, double y3, double y4){
    return y4;
}

double y3dot(double y1, double y2, double y3, double y4){  
    double numerator = g * sin(y2) * cos(y1-y2) - 2 * g * sin(y1) - y3 * y3 * cos(y1-y2) * sin(y1-y2) - y4 * y4 * sin(y1-y2);
    double denominator = 2 - cos(y1-y2) * cos(y1-y2);
    
    return numerator / denominator; 
}

double y4dot(double y1, double y2, double y3, double y4){
    double numerator = g * sin(y1) * cos(y1-y2) - g * sin(y2) + 0.5 * y4 * y4 * cos(y1-y2) * sin(y1-y2) + y3 * y3 * sin(y1-y2);
    double denominator = 1 - 0.5 * cos(y1-y2) * cos(y1-y2);

    return numerator / denominator;
}



int main(){

    FILE *f1 = fopen("posiciones_pendulo.dat", "w");
        if (f1 == NULL) {                                          ///comprobar que el archivo se ha abierto
        fprintf(stderr, "No se pudo abrir el archivo1.\n");
        return 1;
    }
    FILE *f2 = fopen("hamiltoniano.dat", "w");
        if (f2 == NULL) {                                          ///comprobar que el archivo se ha abierto
        fprintf(stderr, "No se pudo abrir el archivo1.\n");
        return 1;
    }

    //// PARAMETROS

    double phi0 = 1.0;                  // Angulo 1 inicial
    double psi0 = 0.0;                  // Angulo 2 inicial
    double phidot0 = 0.0;               // Velocidad Angular 1 inicial    
    double psidot0 = 0.0;               // Velocidad Angular 2 inicial
    double T = 300.0;                   // Tiempo total transcurrido
    double h = 0.01;                    // Paso temporal

    //// VARIABLES

    double Y[4];                        // Y[phi,psi,phidot,psidot] vector de coordenadas y velocidades asociadas
    double k1[4], k2[4], k3[4], k4[4];  // Vectores para la evolucion temporal 
    double t = 0.0;                       // Tiempo
    int i,j;                            // Contadores
    double x1,y1,x2,y2;                 // Posiciones X e Y en un instante t de las dos masas
    double hamiltoniano;

    //// CALCULOS INICIALES


    //// INSTANTE INICIAL

    Y[0] = phi0;                           // Angulo 1 inicial
    Y[1] = psi0;                           // Angulo 2 inicial
    Y[2] = phidot0;                        // Velocidad Angular 1 inicial
    Y[3] = psidot0;                        // Velocidad Angular 2 inicial

    //// CALCULOS INSTANTES SUPERIORES
    while (t<T){

        // k1
        k1[0] = h*y1dot(Y[0], Y[0], Y[2], Y[3]);
        k1[1] = h*y2dot(Y[0], Y[0], Y[2], Y[3]);
        k1[2] = h*y3dot(Y[0], Y[0], Y[2], Y[3]);
        k1[3] = h*y4dot(Y[0], Y[0], Y[2], Y[3]);

        //k2
        k2[0] = h*y1dot(Y[0]+k1[0]/2.0, Y[1]+k1[1]/2.0, Y[2]+k1[2]/2.0,  Y[3]+k1[3]/2.0);
        k2[1] = h*y2dot(Y[0]+k1[0]/2.0, Y[1]+k1[1]/2.0, Y[2]+k1[2]/2.0,  Y[3]+k1[3]/2.0);
        k2[2] = h*y3dot(Y[0]+k1[0]/2.0, Y[1]+k1[1]/2.0, Y[2]+k1[2]/2.0,  Y[3]+k1[3]/2.0);
        k2[3] = h*y4dot(Y[0]+k1[0]/2.0, Y[1]+k1[1]/2.0, Y[2]+k1[2]/2.0,  Y[3]+k1[3]/2.0);  

        //k3
        k3[0] = h*y1dot(Y[0]+k2[0]/2.0, Y[1]+k2[1]/2.0, Y[2]+k2[2]/2.0,  Y[3]+k2[3]/2.0);
        k3[1] = h*y2dot(Y[0]+k2[0]/2.0, Y[1]+k2[1]/2.0, Y[2]+k2[2]/2.0,  Y[3]+k2[3]/2.0);
        k3[2] = h*y3dot(Y[0]+k2[0]/2.0, Y[1]+k2[1]/2.0, Y[2]+k2[2]/2.0,  Y[3]+k2[3]/2.0);
        k3[3] = h*y4dot(Y[0]+k2[0]/2.0, Y[1]+k2[1]/2.0, Y[2]+k2[2]/2.0,  Y[3]+k2[3]/2.0);  

        // k4
        k4[0] = h*y1dot(Y[0]+k3[0], Y[1]+k3[1], Y[2]+k3[2], Y[3]+k3[3]);
        k4[1] = h*y2dot(Y[0]+k3[0], Y[1]+k3[1], Y[2]+k3[2], Y[3]+k3[3]);
        k4[2] = h*y3dot(Y[0]+k3[0], Y[1]+k3[1], Y[2]+k3[2], Y[3]+k3[3]);
        k4[3] = h*y4dot(Y[0]+k3[0], Y[1]+k3[1], Y[2]+k3[2], Y[3]+k3[3]);

        // Actualizar el vector Y
        for (i = 0; i < 4; i++) {
        Y[i] += 1.0/6.0*(k1[i]+k2[i]+k3[i]+k4[i]);
        }

        t += h;

        x1 = sin(Y[0]);
        y1 = -cos(Y[0]);
        x2 = sin(Y[0]) + sin(Y[1]);
        y2 = -cos(Y[0]) -cos(Y[1]);



        ////escribir en el archivo de salida
        fprintf(f1,"%lf,\t%lf\n%lf,\t%lf\n",x1,y1,x2,y2);
        fprintf(f1,"\n");
        fprintf(f2,"%lf\n",hamiltoniano);
    }
return 0;
}