#include <stdio.h>
#include <math.h>
#include <time.h>

//// CONSTANTES
#define g 1           // Aceleracion de la gravedad
#define PI 3.14159265358979323846


//// FUNCIONES
double y1dot(double y1, double y2, double y3, double y4){
    return y3;
}

double y2dot(double y1, double y2, double y3, double y4){
    return y4;
}

double y3dot(double y1, double y2, double y3, double y4){  
    double numerador = g * sin(y2) * cos(y1-y2) - 2 * g * sin(y1) - y3 * y3 * cos(y1-y2) * sin(y1-y2) - y4 * y4 * sin(y1-y2);
    double denominador = 2 - cos(y1-y2) * cos(y1-y2);
    
    return numerador / denominador; 
}

double y4dot(double y1, double y2, double y3, double y4){
    double numerador = g * sin(y1) * cos(y1-y2) - g * sin(y2) + 0.5 * y4 * y4 * cos(y1-y2) * sin(y1-y2) + y3 * y3 * sin(y1-y2);
    double denominador = 1 - 0.5 * cos(y1-y2) * cos(y1-y2);

    return numerador / denominador;
}

//// FUNCION PRINCIPAL
int main(){

    // Variables para registrar el tiempo de inicio y fin
    time_t start, end;

    // Registrar el tiempo de inicio
    time(&start);

    // Abrir archivos de escritura
    FILE *f1 = fopen("posiciones_pendulo.dat", "w");
        if (f1 == NULL) {                                          // Comprobar que el archivo se ha abierto
        fprintf(stderr, "No se pudo abrir el archivo1.\n");
        return 1;
    }

        FILE *f2 = fopen("mapa_poincare_angulos.dat", "w");
        if (f2 == NULL) {                                          // Comprobar que el archivo se ha abierto
        fprintf(stderr, "No se pudo abrir el archivo2.\n");
        return 1;
    }

        FILE *f3 = fopen("mapa_poincare_phi.dat", "w");
        if (f3 == NULL) {                                          // Comprobar que el archivo se ha abierto
        fprintf(stderr, "No se pudo abrir el archivo3.\n");
        return 1;
    }

        FILE *f4 = fopen("mapa_poincare_psi.dat", "w");
        if (f4 == NULL) {                                          // Comprobar que el archivo se ha abierto
        fprintf(stderr, "No se pudo abrir el archivo4.\n");
        return 1;
    }

        FILE *f5 = fopen("espacio_fasico.dat", "w");
        if (f5 == NULL) {                                          // Comprobar que el archivo se ha abierto
        fprintf(stderr, "No se pudo abrir el archivo5.\n");
        return 1;
    }

    //// PARAMETROS

    double phi0 = 4.0*PI/180.0;        // Angulo 1 inicial
    double psi0 = 4.0*PI/180.0;        // Angulo 2 inicial 
    double psidot0 = 0.1;               // Velocidad Angular 2 inicial
    double E = 1.0*g;                   // Energia del sistema
    double d = 1.0;                     // Direccion de la velocidad inicial de la masa 1 (+1 antihorario, -1 horario)
    double T = 200.0;                // Tiempo total transcurrido
    double h = 0.01;                    // Paso temporal

    //// VARIABLES

    double Y[4];                        // Y[phi,psi,phidot,psidot] vector de coordenadas y velocidades asociadas
    double k1[4], k2[4], k3[4], k4[4];  // Vectores para la evolucion temporal 
    double t = 0.0;                     // Tiempo
    int i,j;                            // Contadores
    double x1,y1,x2,y2;                 // Posiciones X e Y en un instante t de las dos masas

    //// CALCULOS INICIALES

    // Velocidad Angular 1 inicial
    double discriminante = psidot0*psidot0*cos(phi0-psi0)*cos(phi0-psi0) -4*(0.5*psidot0*psidot0 - 2*g*cos(phi0) - g*cos(psi0) - E);

    if (discriminante < 0) {
        printf("Error: La expresión bajo la raíz cuadrada es negativa.\n"); 
        return 1;
    }
    double phidot0 = 0.5 * (-psidot0*cos(phi0-psi0) + d*sqrt(discriminante));
        phidot0 = 0.1;                     
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

        // Calcular posiciones x e y de ambas masas
        x1 = sin(Y[0]);
        y1 = -cos(Y[0]);
        x2 = sin(Y[0]) + sin(Y[1]);
        y2 = -cos(Y[0]) -cos(Y[1]);



        // Escribir en los archivos de salida
        fprintf(f1,"%lf,\t%lf\n%lf,\t%lf\n",x1,y1,x2,y2);   // Posiciones x, y de ambas masas
        fprintf(f1,"\n");

        fprintf(f2, "%lf,\t%lf\n",Y[0],Y[1]);               // Mapa Poincare angulos 
        fprintf(f2,"\n");

        fprintf(f3,"%lf,\t%lf\n",Y[0],Y[2]);               // Mapa Poincare phi 
        fprintf(f3,"\n");

        fprintf(f4,"%lf,\t%lf\n",Y[1],Y[3]);               // Mapa Poincare psi 
        fprintf(f4,"\n");

        fprintf(f5,"%lf,\t%lf,\t%lf,\t%lf\n",Y[0],Y[1],Y[2],Y[3]);               // Vector Y

    }

// Cerrar archivos de escritura
fclose(f1);
fclose(f2);
fclose(f3);
fclose(f4);
fclose(f5);


// Registrar el tiempo de finalización
time(&end);

// Calcular el tiempo transcurrido
double tiempotranscurrido = difftime(end, start);
printf("Tiempo transcurrido: %.2f segundos\n", tiempotranscurrido);

return 0;
}
