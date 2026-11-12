# EctoLaser — protótipo de webcam (laboratório)

## Escopo efetivo e limites

A webcam lê o ambiente em tempo real; o OpenCV **detecta rostos sem identificar pessoas** e lê um cartão QR de demonstração escrito “Wicolly”. **Não é reconhecimento facial e não autentica quem está diante da câmera.** O crachá pode ser exibido por qualquer pessoa; o sistema apenas lê seu conteúdo.

O exercício demonstra exatamente o fluxo necessário para os módulos do EctoLaser (captura de câmera → análise de imagem → sobreposição de informações → sinal no Arduino), mas a futura identificação de larvas será feita com **outro modelo YOLO treinado para carrapatos**, não com esse detector de rostos.

Não há coleta, armazenamento, envio ou comparação de fotografias de pessoas, nem download de Instagram. A única imagem gravada opcionalmente é o cartão QR sintético (sem foto).

## Requisitos

- Windows com webcam funcional.
- Python 3.11+ e ambiente virtual com **OpenCV 4.13** (com `QRCodeDetector`, `QRCodeEncoder_create` e `CascadeClassifier`). No Destruking foi validada a webcam com OpenCV 5.0, mas essa versão falhou no teste de `CascadeClassifier` em CI Linux.
- Opcional Arduino UNO com firmware `firmware/uno_ectolaser_status/uno_ectolaser_status.ino` e `pyserial` instalado se usar `--port`.

### Executar o checkout completo do GitHub no notebook

```powershell
cd "$env:USERPROFILE\Downloads"
git clone -b feat/uno-vision-prototype https://github.com/TSWill03/EctoLaser.git EctoLaser-Demo
cd EctoLaser-Demo
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r demo\requirements-demo.txt
.\.venv\Scripts\python.exe demo\webcam_demo.py --make-badge demo\badge_wicolly_demo.png
.\.venv\Scripts\python.exe demo\webcam_demo.py --check-camera --camera 0
.\.venv\Scripts\python.exe demo\webcam_demo.py --camera 0
```

Se você já clonou a branch, mas ainda não instalou as dependências, prepare o ambiente virtual:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r demo\requirements-demo.txt
```

Não utilize `opencv-python 5.0` global para este demo: a classe Haar `cv2.CascadeClassifier` pode não estar disponível nessa versão. O iniciador prepara OpenCV 4.13 em ambiente isolado.

Alternativa: dê duplo clique em `demo/INICIAR_ECTOLASER.bat`. Se a câmera padrão for outra, execute `--camera 1` ou `--camera 2`. Pressione `Q` ou `Esc` para sair. Mostre o QR `badge_wicolly_demo.png` impresso ou pela tela de outro dispositivo à câmera.

### Arduino opcional

Com a placa conectada, firmware compilado/enviado pela IDE Arduino e porta serial conhecida:

```powershell
.\.venv\Scripts\python.exe -m pip install pyserial
.\.venv\Scripts\python.exe demo\webcam_demo.py --camera 0 --port COM5
```

O LED embutido somente pisca quando um rosto está no quadro e o QR de demonstração foi lido recentemente. Isso não constitui verificação de identidade e **não aciona laser, relé, motor ou outro equipamento**.

## Testes de software

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe demo\webcam_demo.py --check-camera --camera 0
.\.venv\Scripts\python.exe demo\webcam_demo.py --camera 0 --headless --max-frames 30
```

A câmera é usada localmente; esses comandos não salvam imagens ou vídeos. O teste da webcam em modo headless só verifica a captura e o pipeline, **não a identificação de Wicolly nem a qualidade de um detector de carrapatos**.

## Instagram

O perfil pessoal informado anteriormente é `@wicolly`. A página pública não foi obtida de forma confiável pelas ferramentas disponíveis. **Nenhuma foto do Instagram foi coletada.** O protótipo não faz correspondência biométrica entre webcam e fotografias de terceiros ou do perfil pessoal.

## Migração para foco original

Após dispor de dataset anotado e de pesos treinados do projeto Roboflow EctoLaser, substituir o detector demonstrativo por detector da classe `cluster_larvas_pasto`, manter webcam/serial como adaptadores e medir precisão/recall. Não conectar dispositivo de eliminação física a este demo.
