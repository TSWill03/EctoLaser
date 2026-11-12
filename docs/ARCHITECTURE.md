# EctoLaser — Arquitetura do protótipo acadêmico v0.2

> **Status: proposta de engenharia + código de integração em branch de desenvolvimento.** Hardware ainda não montado, detector real ainda não treinado, campo ainda não testado.

## Decisão arquitetural

O **Arduino UNO R3 permanece no protótipo**, mas não executa inferência YOLO. O UNO R3 tem apenas **2 kB SRAM e 32 kB flash**; não consegue processar fotografias de alta resolução nem modelos modernos de visão computacional. Sua função é comunicar eventos e controlar exclusivamente indicadores visuais (LED da própria placa) durante o MVP.

Um **computador de borda** faz a captura e inferência: primeiro notebook já disponível; para protótipo autônomo, *Raspberry Pi 5* ou equipamento equivalente, sujeito a benchmarks de latência e energia.

```text
                FOTOS ou CAMERA
                      |
              USB / CSI (host)
                      v
           COMPUTADOR DE BORDA
            Python + OpenCV + YOLO
             classe cluster_larvas_pasto
                      |
              filtro de confiança
              e análise da imagem
                      |
                    USB
                 serial 115200
                      |
                      v
              ARDUINO UNO R3
          LED embutido = indicador
          da detecção (SIMULAÇÃO)
        nenhum laser/rele/atuador
```

## Configuração v0.2 — demonstração de mesa

| Módulo | Elemento | Responsabilidade |
| --- | --- | --- |
| Captura | Webcam USB com foco manual/macro ou câmera compatível com o host | Fotografias próximas do capim; a ótica deve ser validada |
| IA | Notebook (primeira etapa) | Executar YOLO treinado para aglomerados larvais e mostrar caixas nas imagens |
| E/S | Arduino UNO R3 via USB | Receber evento de detecção, piscar LED embutido; não recebe vídeo |
| Alimentação | Notebook via bateria/fonte + Arduino alimentado via USB do notebook | Montagem mínima; energia não vem do UNO para a câmera |
| Energia autônoma (futuro) | Raspberry Pi 5 com fonte/bateria regulada **5 V / 5 A** apropriada | Pi alimenta o UNO pela USB se houver margem elétrica verificada |
| Invólucro | Suporte impresso em 3D para câmera, computador/Arduino e cabos | Evitar contato acidental e melhorar apresentação |

### Energia e ligações seguras

- **Teste inicial:** webcam conectada diretamente ao notebook, Arduino UNO conectado ao notebook por USB. O LED embutido (pino 13) dispensa fiação externa.
- **Teste sem tomada:** usar bateria do notebook. Para demonstrar uma fonte externa dedicada, adicionar um power bank adequado ao **computador de borda** após validar o consumo e a compatibilidade elétrica, ou usar alimentação USB apropriada. Não misturar fontes de 5 V em paralelo sem projeto elétrico.
- **Com Raspberry Pi 5:** utilizar alimentação USB-C especificada como **5 V / 5 A**. Uma bateria USB-C PD qualquer nem sempre negocia 5 V/5 A; validar efetivamente a fonte/cabo. Alimentar o UNO via USB do Pi só após medir o consumo total.
- **Futuro em trator:** isolamento do sistema elétrico do veículo, fusíveis e conversores DC-DC automotivos para proteger contra ruído, picos, vibração e inversão de polaridade. Não ligar diretamente os 12/24 V do trator em pinos de 5 V da placa.
- **Não usar:** pilha retangular de 9 V como fonte principal de computador, alimentação da câmera via pino 5 V do UNO ou saídas com laser no protótipo atual.

## Protocolo serial mínimo

115200 baud; comandos ASCII com terminador `\n`; o UNO aceita somente:

- `PING` → `PONG` (saúde da conexão);
- `INDICATE` → piscar LED da placa por até 600 ms (detecção ou simulação visual);
- `CLEAR` → apagar LED imediatamente.

O comando não implica remoção ou eliminação real. Não há interface de disparo, PWM, motor, servo ou relé. Se a serial para ou comando falha, o indicador apaga por timeout.

## Aplicação host prevista

- Foto com pesos YOLO específicos: `python host/ectolaser_bridge.py --image foto.jpg --weights caminho/modelo.pt --port COM5`.
- Simulação explícita do Arduino (sem detectar nada): `python host/ectolaser_bridge.py --manual-demo --port COM5`.
- Autoteste sem Arduino: `python -m unittest discover -s tests -v`.

A integração de fotos só poderá marcar uma detecção se os pesos forem válidos, o modelo incluir a classe exata `cluster_larvas_pasto` e a previsão ultrapassar o limite. Treino/dados no Roboflow oficial; sem API keys no Git.

## Riscos e critérios para evoluir

1. Detecção do campo não é demonstrada pelo simples acionamento do LED; anotações e resultados de IA precisam de validação separada.
2. Sem modelos treinados para aglomerados larvais, o teste do Arduino é **exclusivamente uma simulação de comunicação**.
3. Aglomerados em capim são pequenos: validar macro/foco, luz, distância, oclusão e velocidade em vídeo real.
4. Laser em pasto apresenta risco de fogo/reflexos/lesões; **fora do circuito desta etapa**. Pesquisar remoção mecânica confinada e requisitos de segurança antes de qualquer tratamento.
5. Migração do MVP anterior em ZIP para o GitHub é tarefa futura; esta branch prova apenas a ligação host–UNO e a escolha de arquitetura.

## Fontes oficiais

- [Arduino UNO R3](https://docs.arduino.cc/hardware/uno-rev3)
- [Ficha do UNO R3, memória e tensão](https://docs.arduino.cc/resources/datasheets/A000066-datasheet.pdf)
- [Alimentação Raspberry Pi 5](https://www.raspberrypi.com/documentation/computers/getting-started.html#power-supply)
- [GitHub EctoLaser](https://github.com/TSWill03/EctoLaser)
- [Roboflow EctoLaser](https://app.roboflow.com/wicolly-wicolly03-alcantara/ectolaser/)
