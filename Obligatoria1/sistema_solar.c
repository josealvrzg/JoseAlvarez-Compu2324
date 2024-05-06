#include <stdio.h>
#include <math.h>

#define PLANETAS 9 //se cambiará este parametro para añadir o quitar planetas
#define G 6.67430e-11  // Constante de gravitación universal en m^3 kg^-1 s^-2
#define Ms 1.989e30 //masa Sol en kg
#define c 149.6e9 //distancia Tierra-Sol en m


int main() {

    int GEO=0; // 0 si queremos modelo Heliocentrico
              // 1 si queremos modelo Geocentrico 


    int N=100000; //iteracionnes
    double dt=0.01;  //precision temporal

    int i, j; //contador

    double t=0; //tiempo
    
    double masas[PLANETAS]; //masas
    
    double R[PLANETAS][2]; //array de posiciones x e y

    double V[PLANETAS][2]; //array de velocidades x e y

    double A[PLANETAS][2]; //aceleracion en t
    double w[PLANETAS][2];

    double E[2]; //Energía potencial y cinética
    double L; //momento angunlar
    
    double P[PLANETAS-1]; //periodo
    double Ranterior[PLANETAS][2]; //se utilizara para calculo del periodo

////////////////////////////////////////////////////////////////////////////// Leer datos iniciales usando fscanf

    // Abrir el archivo
    FILE *f1, *f2, *f3;
    f1 = fopen("datos_iniciales.txt", "r");
    f2 = fopen("planets_data.dat","w");
    f3 = fopen("energias.dat","w");

    if (f1 == NULL) {                                          ///comprobar que el archivo se ha abierto
        fprintf(stderr, "No se pudo abrir el archivo1.\n");
        return 1;
    }
    if (f2 == NULL) {                                          ///comprobar que el archivo se ha abierto
        fprintf(stderr, "No se pudo abrir el archivo2.\n");
        return 1;
    }
    if (f3 == NULL) {                                          ///comprobar que el archivo se ha abierto
        fprintf(stderr, "No se pudo abrir el archivo3.\n");
        return 1;
    }

// masas en kg

    for (i = 0; i < PLANETAS; i++) {

        if (fscanf(f1, "%lf", &masas[i]) != 1) {   //en cada iteracion la informacion que señala el puntero f1 se asigna a masas[i]
            fprintf(stderr, "Error al leer el archivo.\n"); //linea para ver si hay  algun error
            fclose(f1);
            return 1;
        }
    }

    ////////// asegurar que f1 empieza a leer los radios donde debe ser (radio[0]=0)
double x;
fscanf(f1,"%lf", &x);
while(x!=0){
    fscanf(f1,"%lf", &x);  
}

R[0][0]=x;
//////////

/// matriz de posiciones (x,y) inicial en m
for (int i = 1; i < PLANETAS; i++) {
            fscanf(f1, "%lf", &R[i][0]); //f1 ahora apunta a radios[1]
            R[i-1][1] = 0;

        }

    /// asegurar que f1 empieza a leer las velocidades donde debe ser (velocidad[0]=0)
double y;
fscanf(f1,"%lf", &y);
while(y!=0){
    fscanf(f1,"%lf", &y);  
}

V[0][1]=y;

///matriz de velocidades (vx,vx) inicial en m/s
for (int j = 1; j < PLANETAS; j++) {
            fscanf(f1, "%lf", &V[j][1]); //f1 ahora apunta a velocidades[1]
            V[j-1][0] = 0;
        }


//Cambio de escala
for (i=0; i<PLANETAS; i++) 
    {
        masas[i]=masas[i]/Ms;                 //maasa solares
        R[i][0]=R[i][0]/c;                    //unidades astronomicas
        V[i][1]=V[i][1] /sqrt(G*Ms/c);        //unidad temporal 58,1 dias
    }


// Cerrar el archivo de lectura
    fclose(f1);

/////////////////////////////// Geocentrico
double Rtierra[2][2];
Rtierra[0][1]=0;
Rtierra[1][1]=R[3][1];


////////////////////////////////////////////////////////////////////////////// Calculos y guardado de datos con fprintf

////////intante inicial

// guardar en el archivo de salida posiciones iniciales
for ( i = 0; i < PLANETAS; i++)
{
    fprintf(f2,"%lf,\t%lf\n",R[i][0],R[i][1]);
}
    fprintf(f2,"\n");


//calculo primera aceleracion
 double mod;

 for(i=0; i<PLANETAS; i++){
        for (j=0; j<PLANETAS; j++)
        {
            if (j!=i)
            {
                mod=pow(sqrt((R[i][0]-R[j][0])*(R[i][0]-R[j][0])+(R[i][1]-R[j][1])*(R[i][1]-R[j][1])), 3);
                A[i][0]-=masas[j]*(R[i][0]-R[j][0])/mod;
                A[i][1]-=masas[j]*(R[i][1]-R[j][1])/mod;
            }
        }
    }

//calculo energia y momento angular inicial
double d;
for(i=0; i<PLANETAS; i++){
            for (j=i+1; j<PLANETAS; j++)//Suma de energias potenciales
            {
                d=sqrt((R[i][0]-R[j][0])*(R[i][0]-R[j][0])+(R[i][1]-R[j][1])*(R[i][1]-R[j][1]));
                E[0]-=masas[j]*masas[i]/d;
            }
    E[1]+=masas[i]*(V[i][0]*V[i][0]+V[i][1]*V[i][1])/2; //Suma de energias cineticas

    L+=sqrt(R[i][0]*R[i][0]+R[i][1]*R[i][1])*masas[i]*sqrt(V[i][0]*V[i][0]+V[i][1]*V[i][1]);
}


//escribir en energias.data
fprintf(f3,"EPotencial:\tECinetica:\tETotal:\t Momento_Angular:\n%lf,\t%lf,\t%lf,\t%lf\n",E[0],E[1],E[0]+E[1],L);


//////////////////////////////////////////////////////////Calculos instantes superiores

while (t<dt*N)///bucle iteraciones
{



for (i=0; i<PLANETAS; i++)//posiciones en t+dt


        {
            Ranterior[i][0]=R[i][0];
            Ranterior[i][1]=R[i][1];

            R[i][0]=R[i][0]+V[i][0]*dt+A[i][0]*dt*dt/2;
            R[i][1]=R[i][1]+V[i][1]*dt+A[i][1]*dt*dt/2;
            
        }

for (i=0; i<PLANETAS; i++)//w (servirá para calcular la velocidad en t+dt)
        {
            w[i][0]=V[i][0]+A[i][0]*dt/2;    //aceleraciones en t
            w[i][1]=V[i][1]+A[i][1]*dt/2;
            
        }


 for(i=0; i<PLANETAS; i++){///aceletaciones en t+dt
 A[i][0]=0;
 A[i][1]=0;
        for (j=0; j<PLANETAS; j++)
        {
            if (j!=i)
            {
                mod=pow(sqrt((R[i][0]-R[j][0])*(R[i][0]-R[j][0])+(R[i][1]-R[j][1])*(R[i][1]-R[j][1])), 3);
                A[i][0]-=masas[j]*(R[i][0]-R[j][0])/mod;
                A[i][1]-=masas[j]*(R[i][1]-R[j][1])/mod;
            }
        }
    }

for (i=0; i<PLANETAS; i++)//velocidades en t+dt
        {
            V[i][0]=w[i][0]+A[i][0]*dt/2;     //aqui las aceleraciones son en t+dt
            V[i][1]=w[i][1]+A[i][1]*dt/2;
            
        }

//calculo energia y momento en t+dt
E[0]=E[1]=L=0;

for(i=0; i<PLANETAS; i++){
            for (j=i+1; j<PLANETAS; j++)//Suma de energias potenciales
            {
                d=sqrt((R[i][0]-R[j][0])*(R[i][0]-R[j][0])+(R[i][1]-R[j][1])*(R[i][1]-R[j][1]));
                E[0]-=masas[j]*masas[i]/d;
            }

    E[1]+=masas[i]*(V[i][0]*V[i][0]+V[i][1]*V[i][1])/2; //Suma de energias cineticas

    L+=sqrt(R[i][0]*R[i][0]+R[i][1]*R[i][1])*masas[i]*sqrt(V[i][0]*V[i][0]+V[i][1]*V[i][1]); //Momento angular
}


////escribir en el archivo de salida

for ( i = 0; i < PLANETAS; i++) //posiciones
{
    fprintf(f2,"%lf,\t%lf\n",R[i][0],R[i][1]);
    
}
fprintf(f2,"\n");

fprintf(f3,"%lf,\t%lf,\t%lf,\t%lf\n",E[0],E[1],E[0]+E[1],L); //energias y momento

///calculo periodo

for (i=1; i<PLANETAS; i++)
        {
        if ( P[i-1]==0 && Ranterior[i][0]>0 && Ranterior[i][1]<0 &&R[i][0]>=0 && R[i][1]>=0)    //si pasa de cuarto a primer cuadrante por primera vez
        {
        P[i-1]=t ; 
        
        }
        }

t=t+dt;
/// se repite este proceso en numero de iteraciones que queramos
}
fclose(f2);
fclose(f3);


for (i=1; i<PLANETAS; i++){     //imprimir periodos por pantalla
    printf("%lf\n",P[i-1]);
}


return 0; 



}


