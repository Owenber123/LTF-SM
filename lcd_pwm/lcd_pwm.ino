#define LCD_PWM PB0
void setup()
{
  pinMode(LCD_PWM, OUTPUT);
}
void loop()
{
  digitalWrite(LCD_PWM, HIGH);
  delayMicroseconds(100); // 100% duty cycle @ 10KHz
  digitalWrite(LCD_PWM, LOW);
  delayMicroseconds(100 - 100);
}
