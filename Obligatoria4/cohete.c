#include <stdio.h>
#include <math.h>

//// CONSTANTES en el Sitema Internacional
#define G 6.67e-11      // Constante de gravitación universal
#define dTL 3.844e8     // Distancia Tierra-Luna
#define MT 5.9736e24    // Masa de la Tierra
#define ML 0.07349e24   // Masa de la Luna
#define w 2.6617e-6     // Velocidad angular de la Luna
#define RT 6.378160e6   // Radio de la Tierra
#define RL 1.7374e6     // Radio de la Luna
#define PI 3.14159265358979323846
#define m 750e3         // Masa cohete

//// FUNCIONES
double rdot(double Pr){
    return Pr;
}
double phidot(double r, double Pphi){
    return Pphi/(r*r);
}
double Prdot(double r, double phi, double Pphi, double t,double Delta,double mu, double rprim){
    
    return Pphi*Pphi/pow(r,3)-Delta*(1/(r*r)+mu/pow(rprim,3)*(r-cos(phi-w*t))) ;
}
double Pphidot(double r, double phi, double t,double Delta,double mu, double rprim){
    return -Delta*mu/pow(rprim,3)*r*sin(phi-w*t);
}



int main(){

    FILE *f1 = fopen("posiciones_cohete.dat", "w");
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

    double v0 = 11200.0;                // Velocidad inicial
    double phi0 = 30.0*PI/180.0;        // Angulo inicial cohete
    double theta0 = 30.0*PI/180.0;      // Angulo velocidad inicial    
    double h = 45.0;                    // Paso temporal
    double T = 3.0e6;                   // Tiempo total transcurrido

    //// VARIABLES

    double Y[4];                        // Y[r,phi,Pr,Pphi] vector de coordenadas y momentos asociados
    double k1[4], k2[4], k3[4], k4[4];  // Vectores para la evolucion temporal 
    double t = 0;                       // Tiempo
    int i,j;                            // Contadores
    double x,y,xL,yL;                   // Posiciones X e Y en un instante t del cohete y de la Luna
    double hamiltoniano;

    //// CALCULOS INICIALES

    double Delta = G*MT/pow(dTL,3);
    double mu = ML/MT;

    //// INSTANTE INICIAL y REESCALAMIENTO

    Y[0] = RT   /dTL;                           // Radio inicial
    Y[1] = phi0;                                // Angulo inicial
    Y[2] = v0*cos(theta0-phi0)  /dTL;           // Momento Radial inicial
    Y[3] = (RT*v0*sin(theta0-phi0)+RT*RT*2*PI/(24*3600))  /(dTL*dTL);  // Momento Angular inicial masa*radio^2*velocidad angular de la Tierra

    //// CALCULOS INSTANTES SUPERIORES
    while (t<T){

        double rprim = sqrt(1+Y[0]*Y[0]-2*Y[0]*cos(Y[1]-w*t));

        // k1
        k1[0] = h*rdot(Y[2]);
        k1[1] = h*phidot(Y[0],  Y[3]);
        k1[2] = h*Prdot(Y[0],   Y[1],   Y[3],   t, Delta,mu,rprim);
        k1[3] = h*Pphidot(Y[0], Y[1],   t,  Delta,mu,rprim);

        //k2
        k2[0] = h*rdot(Y[2]+k1[2]/2);
        k2[1] = h*phidot(Y[0]+k1[0]/2,  Y[3]+k1[3]/2);
        k2[2] = h*Prdot(Y[0]+k1[0]/2,   Y[1]+k1[1]/2,   Y[3]+k1[3]/2,   t+h/2,  Delta,mu,rprim);
        k2[3] = h*Pphidot(Y[0]+k1[0]/2, Y[1]+k1[1]/2,   t+h/2,  Delta,mu,rprim);  

        //k3
        k3[0] = h*rdot(Y[2]+k2[2]/2);
        k3[1] = h*phidot(Y[0]+k2[0]/2,  Y[3]+k2[3]/2);
        k3[2] = h*Prdot(Y[0]+k2[0]/2,   Y[1]+k2[1]/2,   Y[3]+k2[3]/2,   t+h/2,  Delta,mu,rprim);
        k3[3] = h*Pphidot(Y[0]+k2[0]/2, Y[1]+k2[1]/2,   t+h/2,  Delta,mu,rprim);    

        // k4
        k4[0] = h*rdot(Y[2]+k3[2]);
        k4[1] = h*phidot(Y[0]+k3[0],  Y[3]+k3[3]);
        k4[2] = h*Prdot(Y[0]+k3[0],   Y[1]+k3[1],   Y[3]+k3[3],   t+h, Delta,mu,rprim);
        k4[3] = h*Pphidot(Y[0]+k3[0], Y[1]+k3[1],   t+h,  Delta,mu,rprim);

        // Actualizar el vector Y
        for (i = 0; i < 4; i++) {
        Y[i] += 1.0/6.0*(k1[i]+k2[i]+k3[i]+k4[i]);
        }

        t += h;

        x = Y[0]*cos(Y[1]);
        y = Y[0]*sin(Y[1]);
        xL = cos(w*t);
        yL = sin(w*t);

        double R = Y[0]*dTL, PR = Y[2]*m*dTL, PPHI = Y[4]*m*dTL*dTL;
        double rL = sqrt(R*R+dTL*dTL-2*R*dTL*cos(Y[1]-w*t));
        hamiltoniano = PR*PR/(2*m)+PPHI*PPHI/(2*m*R*R)-G*m*MT/R-G*m*ML/rL - w*PPHI+2e12;

        ////escribir en el archivo de salida
        fprintf(f1,"%lf,\t%lf\n%lf,\t%lf\n",x,y,xL,yL);
        fprintf(f1,"\n");
        fprintf(f2,"%lf\n",hamiltoniano);
    }
return 0;
}