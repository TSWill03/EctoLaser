# EctoLaser — protótipo de webcam (laboratório)

## Escopo efetivo e limites

A webcam lê o ambiente em tempo real; o OpenCV **detecta rostos sem identificar pessoas** e lê um cartão QR de demonstração escrito “Wicolly”. **Não é reconhecimento facial e não autentica quem está diante da câmera.** O crachá pode ser exibido por qualquer pessoa; o sistema apenas lê seu conteúdo.

O exercício demonstra exatamente o fluxo necessário para os módulos do EctoLaser (captura de câmera → análise de imagem → sobreposição de informações → sinal no Arduino), mas a futura identificação de larvas será feita com **outro modelo YOLO treinado para carrapatos**, não com esse detector de rostos.

Não há coleta, armazenamento, envio ou comparação de fotografias de pessoas, nem download de Instagram. A única imagem gravada opcionalmente é o cartão QR sintético (sem foto).

## Requisitos

- Windows com webcam funcional.
- Python 3.11+ e OpenCV com `QRCodeDetector`, `QRCodeEncoder_create` e cascades Haar (no Destruking foi validado OpenCV 5.0).
- Opcional Arduino UNO com firmware `firmware/uno_ectolaser_status/uno_ectolaser_status.ino` e `pyserial` instalado se usar `--port`.

### Executar na cópia já colocada no Destruking

```powershell
cd "C:\Users\Usuario\Downloads\EctoLaser-UNO-Prototipo"
python demo\webcam_demo.py --make-badge demo\badge_wicolly_demo.png
python demo\webcam_demo.py --check-camera --camera 0
python demo\webcam_demo.py --camera 0
```

Alternativa: dê duplo clique em `demo/INICIAR_ECTOLASER.bat`. Se a câmera padrão for outra, execute `--camera 1` ou `--camera 2`. Pressione `Q` ou `Esc` para sair. Mostre o QR `badge_wicolly_demo.png` impresso ou pela tela de outro dispositivo à câmera.

### Arduino opcional

Com a placa conectada, firmware compilado/enviado pela IDE Arduino e porta serial conhecida:

```powershell
python -m pip install pyserial
python demo\webcam_demo.py --camera 0 --port COM5
```

O LED embutido somente pisca quando um rosto está no quadro e o QR de demonstração foi lido recentemente. Isso não constitui verificação de identidade e **não aciona laser, relé, motor ou outro equipamento**.

## Testes de software

```powershell
python -m unittest discover -s tests -v
python demo\webcam_demo.py --check-camera --camera 0
python demo\webcam_demo.py --camera 0 --headless --max-frames 30
```

A câmera é usada localmente; esses comandos não salvam imagens ou vídeos. O teste da webcam em modo headless só verifica a captura e o pipeline, **não a identificação de Wicolly nem a qualidade de um detector de carrapatos**.

## Instagram

O perfil pessoal informado anteriormente é `@wicolly`. A página pública não foi obtida de forma confiável pelas ferramentas disponíveis. **Nenhuma foto do Instagram foi coletada.** O protótipo não faz correspondência biométrica entre webcam e fotografias de terceiros ou do perfil pessoal.

## Migração para foco original

Após dispor de dataset anotado e de pesos treinados do projeto Roboflow EctoLaser, substituir o detector demonstrativo por detector da classe `cluster_larvas_pasto`, manter webcam/serial como adaptadores e medir precisão/recall. Não conectar dispositivo de eliminação física a este demo.
