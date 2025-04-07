import serial
import time
import paho.mqtt.client as mqtt

mqtt_broker = "1.1.1.1"
mqtt_port = 1883
mqtt_topic = "alarma/estado"
mqtt_user = "test"
mqtt_pass = "111"

client = mqtt.Client()
client.username_pw_set(mqtt_user, mqtt_pass)

try:
    client.connect(mqtt_broker, mqtt_port, 1883)
    print("📡 MQTT conectado")
except Exception as e:
    print(f"❌ Error conectando a MQTT: {e}")

patrones = {
    "DESARMADO": [[248, 0, 0, 0, 128, 248]],
    "ARMADO_TOTAL": [
        [248, 120, 0, 0, 0, 128, 248, 0, 0, 0, 0, 0],
        [120, 0, 0, 0, 0, 0, 248, 120, 0, 0, 0, 128]
    ],
    "DESARMADO EN CASA": [
        [248, 128, 120, 0, 255, 0, 0, 128, 248],
        [248, 128, 120, 224, 0, 0, 128, 248],
        [248, 248, 120, 224, 0, 0, 128, 248],
        [248, 248, 0, 0, 0, 128, 248]
    ],
    "EN CASA 2": [
        [248, 128, 0, 0, 0, 0, 0, 0, 248, 128]
    ]
}

def detectar_estado(payload):
    for estado, patrones_estado in patrones.items():
        for patron in patrones_estado:
            for i in range(len(payload) - len(patron) + 1):
                if payload[i:i+len(patron)] == patron:
                    return estado, patron
    return "DESCONOCIDO", None

def main():
    puerto = "/dev/ttyUSB0"
    baudios = 9600
    ser = serial.Serial(puerto, baudios, timeout=1)
    print(f"🛰️ Escuchando en {puerto} a {baudios} baudios...")

    try:
        while True:
            data = ser.read(29)
            if data:
                payload = list(data)
                print(f"📡 Payload (dec): {payload}")
                estado, patron = detectar_estado(payload)
                if estado != "DESCONOCIDO":
                    print(f"✅ Coincidencia con patrón de {estado}: {patron}")
                    print(f"🔐 Estado evaluado: {estado}")
                    client.publish(mqtt_topic, estado)
                    print(f"📤 Publicando a MQTT → Tópico: {mqtt_topic} | Estado: {estado}")
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("\n🛑 Finalizado por el usuario.")
    finally:
        ser.close()

if __name__ == "__main__":
    main()
