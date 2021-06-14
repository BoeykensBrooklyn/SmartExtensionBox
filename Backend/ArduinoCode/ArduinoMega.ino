#include <EEPROM.h>

//Declaratie drukknoppen
#pragma region Declaratie Drukknoppen
int IKnop1 = 2;
int Iknop2 = 3;
int IKnop3 = 4;
int IKnop4 = 5;
int IKnop5 = 6;
int IKnop6 = 7;
int IKnop7 = 8;
int IKnop8 = 9;
#pragma endregion

//Declaratie Uitgangen
#pragma region Declaratie Uitgangen
int QUitgang1 = 22;
int QUitgang2 = 23;
int QUitgang3 = 24;
int QUitgang4 = 25;
int QUitgang5 = 26;
int QUitgang6 = 27;
int QUitgang7 = 28;
int QUitgang8 = 29;
#pragma endregion

//Variabelen voor de Drukknoppen + Uitgangen
#pragma region Variabelen Voor Drukknoppen + Uitgangen
//Drukknop 1 Variabelen
bool btnState1 = HIGH;
bool btnPrevState1 = HIGH;
bool QState1 = LOW;

//Drukknop 2 Variabelen
bool btnState2 = HIGH;
bool btnPrevState2 = HIGH;
bool QState2 = LOW;

//Drukknop 3 Variabelen
bool btnState3 = HIGH;
bool btnPrevState3 = HIGH;
bool QState3 = LOW;

//Drukknop 4 Variabelen
bool btnState4 = HIGH;
bool btnPrevState4 = HIGH;
bool QState4 = LOW;

//Drukknop 5 Variabelen
bool btnState5 = HIGH;
bool btnPrevState5 = HIGH;
bool QState5 = LOW;

//Drukknop 6 Variabelen
bool btnState6 = HIGH;
bool btnPrevState6 = HIGH;
bool QState6 = LOW;

//Drukknop 7 Variabelen
bool btnState7 = HIGH;
bool btnPrevState7 = HIGH;
bool QState7 = LOW;

//Drukknop 8 Variabelen
bool btnState8 = HIGH;
bool btnPrevState8 = HIGH;
bool QState8 = LOW;
#pragma endregion

//Declaratie Variabelen Voor Seriële Communicatie
String incomingString;

//Declaratie Voor current Sensor ACS712
#include <Filters.h>

#define ACS_Pin A0

float ACS_Value;
float testFrequency = 50;
float windowLength = 40.0 / testFrequency;

float intercept = -0.10;
float slope = 0.07344;

float Amps_TRMS;
float verbruik;

unsigned long printPeriod = 1000;
unsigned long previousMillis = 0;

void setup()
{
    // put your setup code here, to run once:
    //Het aanmaken van input voor de drukknoppen
#pragma region Pinmode Inputs
    pinMode(IKnop1, INPUT_PULLUP);
    pinMode(Iknop2, INPUT_PULLUP);
    pinMode(IKnop3, INPUT_PULLUP);
    pinMode(IKnop4, INPUT_PULLUP);
    pinMode(IKnop5, INPUT_PULLUP);
    pinMode(IKnop6, INPUT_PULLUP);
    pinMode(IKnop7, INPUT_PULLUP);
    pinMode(IKnop8, INPUT_PULLUP);
#pragma endregion

    //Het aanmaken van de output voor de uitgangen
#pragma region Pinmode Outputs
    pinMode(QUitgang1, OUTPUT);
    pinMode(QUitgang2, OUTPUT);
    pinMode(QUitgang3, OUTPUT);
    pinMode(QUitgang4, OUTPUT);
    pinMode(QUitgang5, OUTPUT);
    pinMode(QUitgang6, OUTPUT);
    pinMode(QUitgang7, OUTPUT);
    pinMode(QUitgang8, OUTPUT);
#pragma endregion

    //Open Seriële Poort
    Serial.begin(9600);
    Serial1.begin(9600);

    //Input current sensor
    pinMode(ACS_Pin, INPUT);

    //States ophalen uit EEPROM
    QState1 = EEPROM.read(0);
    QState2 = EEPROM.read(1);
    QState3 = EEPROM.read(2);
    QState4 = EEPROM.read(3);
    QState5 = EEPROM.read(4);
    QState6 = EEPROM.read(5);
    QState7 = EEPROM.read(6);
    QState8 = EEPROM.read(7);
}

void loop()
{
    // put your main code here, to run repeatedly:
    RunningStatistics inputStats;
    inputStats.setWindowSecs(windowLength);
// --------Drukknoppen Inlezen----------
#pragma region drukknop
    // Drukknop 1 Toggle gedeelte
    btnState1 = digitalRead(IKnop1);
    delay(100);
    if (btnState1 != btnPrevState1)
    {
        if (btnState1 == LOW)
        {
            QState1 = !QState1;
            Serial1.println("Knop1:" + String(QState1));
            Serial.println("Knop1:" + String(QState1));
        }
    }
    btnPrevState1 = btnState1;
    EEPROM.put(0, QState1);
    digitalWrite(QUitgang1, QState1);

    // Drukknop 2 Toggle gedeelte
    btnState2 = digitalRead(Iknop2);
    delay(100);
    if (btnState2 != btnPrevState2)
    {
        if (btnState2 == LOW)
        {
            QState2 = !QState2;
            Serial1.println("Knop2:" + String(QState2));
        }
    }
    btnPrevState2 = btnState2;
    EEPROM.put(1, QState2);
    digitalWrite(QUitgang2, QState2);

    // Drukknop 3 Toggle gedeelte
    btnState3 = digitalRead(IKnop3);
    delay(100);
    if (btnState3 != btnPrevState3)
    {
        if (btnState3 == LOW)
        {
            QState3 = !QState3;
            Serial1.println("Knop3:" + String(QState3));
        }
    }
    btnPrevState3 = btnState3;
    EEPROM.put(2, QState3);
    digitalWrite(QUitgang3, QState3);

    // Drukknop 4 Toggle gedeelte
    btnState4 = digitalRead(IKnop4);
    delay(100);
    if (btnState4 != btnPrevState4)
    {
        if (btnState4 == LOW)
        {
            QState4 = !QState4;
            Serial1.println("Knop4:" + String(QState4));
        }
    }
    btnPrevState4 = btnState4;
    EEPROM.put(3, QState4);
    digitalWrite(QUitgang4, QState4);

    // Drukknop 5 Toggle gedeelte
    btnState5 = digitalRead(IKnop5);
    delay(100);
    if (btnState5 != btnPrevState5)
    {
        if (btnState5 == LOW)
        {
            QState5 = !QState5;
            Serial1.println("Knop5:" + String(QState5));
        }
    }
    btnPrevState5 = btnState5;
    EEPROM.put(4, QState5);
    digitalWrite(QUitgang5, QState5);

    // Drukknop 6 Toggle gedeelte
    btnState6 = digitalRead(IKnop6);
    delay(100);
    if (btnState6 != btnPrevState6)
    {
        if (btnState6 == LOW)
        {
            QState6 = !QState6;
            Serial1.println("Knop6:" + String(QState6));
        }
    }
    btnPrevState6 = btnState6;
    EEPROM.put(5, QState6);
    digitalWrite(QUitgang6, QState6);

    // Drukknop 7 Toggle gedeelte
    btnState7 = digitalRead(IKnop7);
    delay(100);
    if (btnState7 != btnPrevState7)
    {
        if (btnState7 == LOW)
        {
            QState7 = !QState7;
            Serial1.println("Knop7:" + String(QState7));
        }
    }
    btnPrevState7 = btnState7;
    EEPROM.put(6, QState7);
    digitalWrite(QUitgang7, QState7);

    // Drukknop 8 Toggle gedeelte
    btnState8 = digitalRead(IKnop8);
    delay(100);
    if (btnState8 != btnPrevState8)
    {
        if (btnState8 == LOW)
        {
            QState8 = !QState8;
            Serial1.println("Knop8:" + String(QState8));
        }
    }
    btnPrevState8 = btnState8;
    EEPROM.put(7, QState8);
    digitalWrite(QUitgang8, QState8);
#pragma endregion drukknop

    // --------Seriële Communicatie -----------
    if (Serial1.available() > 0)
    {
        incomingString = Serial1.readString();
        Serial.println(incomingString.substring(0, 8));

#pragma region Current Sensor
        if (incomingString.substring(0, 8) == "Verbruik")
        {

            ACS_Value = analogRead(ACS_Pin);
            inputStats.input(ACS_Value);

            if ((unsigned long)(millis() - previousMillis) >= printPeriod)
            {
                previousMillis = millis();

                Amps_TRMS = -0.10 + 0.07344 * inputStats.sigma();

                // Watt => P = U . I
                // Voltage => 230V
                verbruik = 230 * Amps_TRMS;
                Serial1.println("Verbruik:" + String(verbruik));
                Serial.println("Amps:" + String(Amps_TRMS));
                Serial.println("Verbruik:" + String(verbruik));
            }
        }
#pragma endregion

        // Schakelen van uitgang1
#pragma region Schakel Uitgang1
        if (incomingString.substring(0, 5) == "Knop1")
        {
            if (incomingString.substring(5, 9) == "Aan")
            {
                QState1 = HIGH;
            }
            else if (incomingString.substring(5, 9) == "Uit")
            {
                QState1 = LOW;
            }
            Serial1.println("Ok");
            Serial.println("Ok");
        }
#pragma endregion

        // Schakelen van uitgang2
#pragma region Schakel Uitgang2
        if (incomingString.substring(0, 5) == "Knop2")
        {
            if (incomingString.substring(5, 9) == "Aan")
            {
                QState2 = HIGH;
            }
            else if (incomingString.substring(5, 9) == "Uit")
            {
                QState2 = LOW;
            }
            Serial1.println("Ok");
        }
#pragma endregion

        // Schakelen van uitgang3
#pragma region Schakel Uitgang3
        if (incomingString.substring(0, 5) == "Knop3")
        {
            if (incomingString.substring(5, 9) == "Aan")
            {
                QState3 = HIGH;
            }
            else if (incomingString.substring(5, 9) == "Uit")
            {
                QState3 = LOW;
            }
            Serial1.println("Ok");
        }
#pragma endregion

        // Schakelen van uitgang4
#pragma region Schakel Uitgang4
        if (incomingString.substring(0, 5) == "Knop4")
        {
            if (incomingString.substring(5, 9) == "Aan")
            {
                QState4 = HIGH;
            }
            else if (incomingString.substring(5, 9) == "Uit")
            {
                QState4 = LOW;
            }
            Serial1.println("Ok");
        }
#pragma endregion

        // Schakelen van uitgang5
#pragma region Schakel Uitgang5
        if (incomingString.substring(0, 5) == "Knop5")
        {
            if (incomingString.substring(5, 9) == "Aan")
            {
                QState5 = HIGH;
            }
            else if (incomingString.substring(5, 9) == "Uit")
            {
                QState5 = LOW;
            }
            Serial1.println("Ok");
        }
#pragma endregion

        // Schakelen van uitgang6
#pragma region Schakel Uitgang6
        if (incomingString.substring(0, 5) == "Knop6")
        {
            if (incomingString.substring(5, 9) == "Aan")
            {
                QState6 = HIGH;
            }
            else if (incomingString.substring(5, 9) == "Uit")
            {
                QState6 = LOW;
            }
            Serial1.println("Ok");
        }
#pragma endregion

        // Schakelen van uitgang7
#pragma region Schakel Uitgang7
        if (incomingString.substring(0, 5) == "Knop7")
        {
            if (incomingString.substring(5, 9) == "Aan")
            {
                QState7 = HIGH;
            }
            else if (incomingString.substring(5, 9) == "Uit")
            {
                QState7 = LOW;
            }
            Serial1.println("Ok");
        }
#pragma endregion

        // Schakelen van uitgang8
#pragma region Schakel Uitgang8
        if (incomingString.substring(0, 5) == "Knop8")
        {
            if (incomingString.substring(5, 9) == "Aan")
            {
                QState8 = HIGH;
            }
            else if (incomingString.substring(5, 9) == "Uit")
            {
                QState8 = LOW;
            }
            Serial1.println("Ok");
        }
#pragma endregion

        //Informatie geven van de Waardes:
#pragma region Stuur String met waardes terug
        if (incomingString.substring(0, 5) == "Value")
        {
            Serial1.println("Values:Knop1:" + String(QState1) + "Knop2:" + String(QState2) + "Knop3:" + String(QState3) + "Knop4:" + String(QState4) + "Knop5:" + String(QState5) + "Knop6:" + String(QState6) + "Knop7:" + String(QState7) + "Knop8:" + String(QState8));
        }
#pragma endregion

        // Test Seriële communicatie
#pragma region teststring

        if (incomingString == "Test")
        {
            Serial1.println("test geslaagd");
            Serial.println("Test geslaagd");
        }
    }
#pragma endregion
}