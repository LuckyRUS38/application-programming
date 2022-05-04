#include <iostream>
using namespace std;

int main()
{
    int N, Lift, Ladder = 0, Time = 0, RubBcego = 650, CallLift = 50, FloorLift = 100, LiftTime = 15, LadderTime = 40, Rub = 0, RubMed = 0, K = 0, RE = 0, Euro;
    string Shop;
    cin >> N >> K >> RE;

    if (RubBcego >= 150)
    {
        RubBcego -= CallLift;
        Rub += CallLift;
    }
    for (Lift; 0 < RubBcego; Lift++)
    {
        RubBcego -= FloorLift;
        Time += LiftTime;
        N--;
        Rub += FloorLift;
    }
    if (N > 0 && RubBcego == 0)
    {
        for (Ladder; N != 0; Ladder++)
        {
            if (Ladder >= 2 && Ladder % 2 == 0)
            {
                LadderTime += 5;
            }
            N--;
            Time += LadderTime;
        }
    }

    RubMed += 250 * 4;
    RubMed += 750 + 99;
    RubMed += 5000 * 2;
    RubMed += 100 * ((K * 2) + (RE + K + RE));

    Euro = 281.11;
    int cu = (300 * 150) + (Euro * 15) + (Euro * 5) + 13500;
    int dns = (59999 + 8999) + (500 + 185);

    if (dns > cu){
        Shop = "DNS";
    }
    else {
        Shop = "Computeruniverse.net";
    }

    cout << Lift << " " << Ladder << " " << Rub << " " << Time << " " << RubMed << " " << Shop;
}
