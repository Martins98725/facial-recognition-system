

🤖 **Sistema de Trava Elétrica com Reconhecimento Facial**
Este projeto implementa um sistema de controle de acesso que utiliza uma webcam para reconhecer rostos e acionar uma trava elétrica através de um Arduino e um módulo relé. É uma solução de automação residencial "faça você mesmo" para permitir acesso sem o uso de chaves.

✨ Funcionalidades Principais
Reconhecimento Facial em Tempo Real: Utiliza a webcam para detectar e identificar rostos continuamente.
<ul>
  <li>Cadastro Dinâmico de Usuários: Um script dedicado permite cadastrar novos rostos de forma interativa, sem precisar alterar o código principal.
</li>
  <li>Autorização Automática: O sistema automaticamente autoriza qualquer pessoa que tenha sido cadastrada, lendo as pastas de usuários no diretório dataset.
</li>
  <li>Feedback Visual: Desenha um retângulo e os pontos faciais (landmarks) sobre o rosto detectado, com cores diferentes para status (Autorizado, Desconhecido).
</li>
  <li>Integração com Hardware: Comunica-se via porta Serial com um Arduino para acionar hardware externo (trava elétrica).
</li>
  <li>Sistema de Cooldown: Evita que a trava seja acionada repetidamente em um curto período de tempo.
</li>
</ul>






🛠️ Tecnologias Utilizadas
Hardware
<ul>
  <li>
    Computador com Webcam (Windows ou Linux)
 </li>
  <li>Arduino UNO (ou similar)</li>
  <li>Módulo Relé de 1 Canal (5V)</li>
  <li>Trava Elétrica Solenoide (12V)</li>
  <li>Fonte de Alimentação Externa (12V)</li>
  <li>Fios Jumper e Cabo USB</li>
</ul>

Software e Bibliotecas
Python 3

<ul>
  <li>face_recognition: Para a lógica de reconhecimento facial.</li>
   <li>opencv-python: Para captura e manipulação de imagem da webcam.</li>
   <li>numpy: Dependência principal do face_recognition.</li>
   <li>pyserial: Para comunicação serial entre Python e Arduino.</li>
   <li>Arduino (C/C++)</li>
</ul>




⚙️ Instalação e Configuração
Siga estes passos para configurar o ambiente e executar o projeto.

1. Pré-requisitos
Python 3 instalado no seu computador.

Arduino IDE instalada.

Todo o hardware listado acima.

2. Montagem do Hardware
Conecte os componentes físicos conforme o diagrama abaixo. Execute esta etapa com todas as fontes de energia desligadas!

Arduino e Relé:

Pino 5V (Arduino) -> VCC (Relé)

Pino GND (Arduino) -> GND (Relé)

Pino Digital 7 (Arduino) -> IN (Relé)

Circuito da Trava (12V):

Positivo (+) da Fonte 12V -> Parafuso COM do Relé.

Parafuso NO (Normally Open) do Relé -> Positivo (+) da Trava.

Negativo (-) da Trava -> Negativo (-) da Fonte 12V.

3. Configuração do Arduino
Conecte o Arduino ao computador via USB.

Abra o arquivo tranca_facial_arduino.ino na Arduino IDE.

Vá em Ferramentas > Placa e selecione "Arduino UNO".

Vá em Ferramentas > Porta e selecione a porta serial correta (ex: COM3, /dev/ttyACM0). Anote esta porta.

Clique em "Carregar" (ícone de seta) para enviar o código para a placa.

4. Configuração do Ambiente Python
Clone ou baixe os arquivos deste projeto para uma pasta no seu computador.

Abra um terminal ou prompt de comando nessa pasta.

`python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate`

Instale todas as dependências Python de uma vez:
`pip install -r requirements.txt`


🚀 Como Usar o Sistema
O uso é dividido em dois passos simples:

Passo 1: Cadastrar um Novo Rosto
Para adicionar uma pessoa ao sistema, execute o script de cadastro no seu terminal:

`python cadastrar_rosto.py`

O programa pedirá um nome de usuário (use nomes simples, como Joao_Silva). Siga as instruções na tela para posicionar o rosto e salvar as fotos de referência.


Passo 2: Ativar a Tranca
Com os usuários já cadastrados, execute o script principal para iniciar o monitoramento:

`python tranca_facial.py`

⚠️ Aviso de Segurança
<ul>
  <li>Manuseie a fonte de 12V com cuidado. Certifique-se de que ela está desligada da tomada ao fazer ou alterar conexões.
</li>
  <li>Nunca alimente a trava elétrica diretamente com o Arduino. Use sempre um relé como intermediário.
</li>
  <li>Este é um projeto para fins educacionais. A segurança do reconhecimento facial pode ser burlada (ex: com uma foto). Não o utilize como única forma de segurança para locais críticos.
</li>
</ul>



💡 Possíveis Melhorias

<ul>
  <li>Adicionar um botão físico para acionamento manual da trava.
</li>
  <li>Implementar um sistema de logs para registrar quem acessou e quando.
</li>
  <li>Adicionar "detecção de vivacidade" (liveness detection) para aumentar a segurança contra ataques com fotos.
</li>
  <li>Integrar notificações via e-mail ou Telegram para avisar sobre acessos.
</li>
  <li>Criar um case impresso em 3D para proteger o circuito.
</li>
</ul>


Autor: **Ícaro Martins** e **Tharcylâine Camilly** 
