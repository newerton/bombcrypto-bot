<h1 align="center">

![Bomb Crypto Banner](https://raw.githubusercontent.com/newerton/bombcrypto-bot/main/images/readme/banner.jpg)

  <a>
    💣 Bomb Crypto Bot 💣 
  </a>
</h1>

## ⚠️ Aviso

Não me responsabilizo por eventuais penalidades sofridas por quem usar o bot, use por sua própria conta e risco.  

## 📌 Glossário

  * [Sobre](#about)
  * [Doação](#donation)
  * [Robô - Previsualização](#robot-preview)
  * [Instalação](#installation)
    * [Comandos no terminal](#commands)
  * [Como funciona](#how-to-works)
  * [Testes](#tests)
  * [Temas](#themes)
  * [Configurações](#configs)
  * [Como configurar o bot](#how-config-bot)
    * [Quais são os problemas](#what-are-problems)
    * [Threshold no arquivo de configuração](#threshold-config)
    * [Substituição das imagens targets](#image-replacement)
    * [Alguns comportamentos que podem indicar um falso positivo ou negativo](#some-behaviors)

## 📋 <a id="about"></a>Sobre

Este bot contêm códigos de outros desenvolvedores, esse bot foi somente refatorado, para facilitar novas implementações e manutenções.  

Desenvolvedores:
* https://github.com/mpcabete/
* https://github.com/afkapp/

Este bot é grátis e de código aberto.

Recursos:  
* Refatoração do código
* Adicionado os 3 captchas
* Temas
* Multi conta com janelas lado a lado e muitas janelas maximizadas
* Rodar o Bot, sem interrupção por erro
* Terminal colorido
* Velocidade no Bot, ganho de alguns minutos nas tarefas
* Aatualização obrigatório do arquivo de configuração
## 🎁 <a id="donation"></a>Doação
BCOIN: 0x4847C29561B6682154E25c334E12d156e19F613a  
PIX: 08912d17-47a6-411e-b7ec-ef793203f836  

## 🤖 <a id="robot-preview"></a>Robô - Previsualização
![Screenshot - Preview](https://raw.githubusercontent.com/newerton/bombcrypto-bot/main/images/readme/bot_working.jpg)

## 🪟 <a id="installation"></a>Instalação

🖥️ Computador/Notebook com Alto e Média configuração  
🐍 Instalar o Python 3.9.9

🖥️ Computador/Notebook com Baixa configuração or baixa configuração com Windows 7 Pro  
🐍 Instalar o Python 3.8.10

🔗 [https://www.python.org/downloads/](https://www.python.org/downloads/)


⚠️ **É importante marcar a opção para adicionar o python ao PATH**  

### <a id="commands"></a>Commands
Instale as dependências, executando o comando abaixo, dentro da pasta do projeto:  

```
pip install -r requirements.txt
```
Pronto! Agora é só iniciar o bot com o comando, dentro da pasta do projeto  

```
python index.py
```


### <a id="how-to-works"></a>**Como funciona?**

O bot não altera nada do código fonte do jogo, ele somente tira print da tela do
game para encontrar os botões e simula movimentos do mouse.

### ⚠️ Algumas configurações podem ser mudadas no arquivo /config/config.yaml, não se esqueça de reiniciar o bot caso mude as configuraçoes, algumas alterações no arquivo /config/config.yaml, pode fazer o bot parar, como por exemplo ativar o telegram quando o bot estiver em execução.

## 🧪 <a id="tests"></a>Testes
**Desktop com médio configuração**  
Intel i5-3570k @ 3.4Ghz, 24GB RAM  
Windows 11, Resolução@1920x1080  
Python 3.9.9  

**Notebook com baixa configuração**  
Laptop Samsumg RV411, Pentium P6200 @ 2.13Ghz, 2GB RAM  
Windows 7, Resolução@1366x768  
Python 3.8.10

## 🎨 <a id="themes"></a>Temas
|      theme     	| toolbar image preview 	|
|:-------------:	|:-----:	|
| default 	| ![Lunar New Year](https://raw.githubusercontent.com/newerton/bombcrypto-bot/main/images/readme/themes/default.jpg)	|
| lunar_newyear 	| ![Lunar New Year](https://raw.githubusercontent.com/newerton/bombcrypto-bot/main/images/readme/themes/lunar_newyear.jpg)	|

## ⚒️ <a id="configs"></a>Configurações
|      código     	| tipo 	| descrição 	|
|:-------------:	|:-----:	|:-----:	|
| **app** | - | - |
| theme | string | Tema atual do jogo, para reconhecer os titulos de erros e lista de heróis. Valores na tabela de [temas](#themes) |
| verify_version | bollean - true/false | Verificar a versão do app a cada 1h, recomendado para manter atualizado |
| emoji | bollean - true/false | Ativar/Desativar mostrar emoji nas mensagens do console |
| terminal_colorful | bollean - true/false | Ativar/Desativar mostrar mensagens coloridas no terminal |
| run_time_app |  int | Tempo de execução do loop do bot |
| monitor_to_use | int | Monitor que o bot usa como referência |
| captcha |  bollean - true/false | Ativar/Desativar o reconhecimento do captcha no jogo |
| speed | string - normal/fast | Dois modos de velocidade do bot, o modo fast é entre 1~3 minutos mais rápido |
| **multi_account** | - | - |
| enable | bollean - true/false | Ativar/Desaativar a funcionalidade de Multi Account  |
| window_title | string | Título da janela, para identificação do jogo ativo pelo bot |
| window_fullscreen | bollean - true/false | Ativar/Desativar o modo Fullscreen, recomendado para monitores pequenos |
| **time_intervals** | - | - |
| send_heroes_for_work | array - [int, int] | Intervalo inicial e final para o bot buscar heróis para trabalhar |
| refresh_heroes_positions | array - [int, int] | Intervalo inicial e final para o bot atualizar o mapa |
| interval_between_movements | array - [int, int] | Tempo em segundos, da pausa dos movimentos do mouse (pyautogui.PAUSE) |
| **chests** | - | - |
| **values** | - | - |
| chest_01 | decimal | Valor de recompensa do baú de marrom |
| chest_02 | decimal | Valor de recompensa do baú de roxo |
| chest_03 | decimal | Valor de recompensa do baú de dourado |
| chest_04 | decimal | Valor de recompensa do baú de azul |
| **threshold** | - | **Valor de confiança do bot em comparação dos targets<br />com as imagens do jogo. Valor minímo é 0 e o máximo é 1.<br />0 - qualquer imagem semelhante<br>0.1 até 0.9 - grau de confiança<br>1 - imagem idêntica sem imperfeição** |
| default | decimal | Valor padrão de confiança |
| error_message | decimal | Valor de confiança do título da janela de erro |
| back_button | decimal | Valor de confiança do botão de voltar do mapa |
| heroes_green_bar | decimal | Valor de confiança da barra parcial de energia do herói |
| heroes_full_bar | decimal | Valor de confiança da barra completa de energia do herói |
| heroes_send_all | decimal | Valor de confiança do botão de enviar todos para trabalhar |
| chest | decimal | Valor de confiança dos baús, para calcular o total de BCOINS do mapa |
| **heroes** | - | - |
| mode | string - all, green, full | Modo de enviar os heróis para o trabalho.<br />**all** - Envia todos os heróis, sem critério.<br />**green** - Envia os heróis com energia parcialmente verde<br />**full** - Envia os heróis com energia completa|
| **list** | - | - |
| scroll_attempts | int | Total de rolagem que o bot vai fazer na lista de heróis |
| click_and_drag_amount | int | Valor máximo que o bot vai fazer a rolagem da lista de heróis |
| **offsets** | - | - |
| work_button_green | array - [int, int] | Offset para o click do mouse no botão de WORK |
| work_button_full | array - [int, int] | Offset para o click do mouse no botão de WORK |
| **metamask** | - | - |
| enable_login_metamask | bollean - true/false | Ativar/Desativar o auto login da Metamask |
| password | string | Senha para desbloquear a Metamask para logar no jogo |
| **services** | - | - |
| telegram | bollean - true/false | Ativar/Desativar o serviço de envio de mensagem para o Telegram |
| **log** | |
| save_to_file | bollean - true/false | Ativar/Desativar salvar o log do console no arquivo logger.log |
| debug | bollean - true/false | Ativar/Desativar a depuração de algumas informações do bot |



## ⚠️ <a id="how-config-bot"></a>Ajustando o bot

**Por que uns ajustes podem ser necessários?**

O bot usa reconhecimento de imagem para tomar decisões e movimentar o mouse e
clicar nos lugares certos.  
Ele realiza isso comparando uma imagem de exemplo com um screenshot da tela do
computador/laptop.  
Este método está sujeito a inconsistências devido a diferenças na resolução da
sua tela e de como o jogo é renderizado no seu computador.
É provável que o bot não funcione 100% na primeira execução, e que você precise fazer alguns ajustes no arquivo de configuração.

<a id="what-are-problems"></a>  

**Quais são os problemas?**

* **Falso negativo** - O bot deveria reconhecer uma imagem, por exemplo, o botão de mandar para trabalhar, mas não reconheceu a imagem na screenshot.

* **Falso positivo** - O bot pensa que reconheceu a imagem que está procurando em um lugar em que esta imagem não aparece.

Para resolver estes problemas existem duas possibilidades, a regulagem do
parâmetro "threshold" no arquivo config.yaml ou a substituição da imagem de
exemplo na pasta "targets" para uma tirada no seu próprio computador:

  <a id="threshold-config"></a>
  ### **Threshold no arquivo de configuração**

  O parâmetro "threshold" regula o quanto o bot precisa estar confiante para
  considerar que encontrou a imagem que está procurando.
  Este valor de 0 a 1 (0% a 100%).
  Ex:

  Um threshold de 0.1 é muito baixo, ele vai considerar que encontrou a imagem
  que esta procurando em lugares que ela não está aparecendo ( falso positivo ).
  O comportamento mais comum pra esse problema é o bot clicando em lugares
  aleatórios pela tela. 


  Um threshold de 0.99 ou 1 é muito alto, ele não vai encontrar a imagem que
  está procurando, mesmo quando ela estiver aparecendo na tela. O comportamento
  mais comum é ele simplesmente não mover o cursor para lugar nenhum, ou travar
  no meio de um processo, como o de login.

  <a id="image-replacement"></a>

  ### **Substituição das imagens targets**

  As imagens exemplo são armazenadas na pasta "images/themes/default". Estas imagens foram tiradas no meu computador com resolução de 1920x1080. Para substituir alguma imagem que não esta sendo reconhecida propriamente, simplesmente encontre a imagem correspondente na pasta "images/themes/default",
  tire um screenshot da mesma área e substitua a imagem anterior. É importante
  que a substituta tenha o mesmo nome, incluindo a extensão .png

  <a id="some-behaviors"></a>

### **Alguns comportamentos que podem indicar um falso positivo ou negativo**

#### Falso positivo:

- Repetidamente enviando um herói que já esta trabalhando para trabalhar em um
  loop infinito.
  - Falso positivo na imagem "work_button.png", o bot acha que esta vendo o botão
    escuro em um herói com o botão claro.

- Clicando em lugares aleatórios(geralmente brancos) na tela
  - Falso positivo na imagem "metamask_sign_button.png"
 
 #### Falso negativo:

- Não fazendo nada
	- Talvez o bot esteja tendo problemas com a sua resolução e não esta reconhecendo nenhuma das imagens, tente mudar a configuração do navegador para 100%.

- Não enviando os heróis para trabalhar
	- Pode ser um falso negativo na imagem "bar_green_stamina.png" caso a opção "heroes.mode" estiver como "green".

## 👍 Curtiu? Dê aquela fortalecida :)

### BCOIN: 0x4847C29561B6682154E25c334E12d156e19F613a  
### PIX: 08912d17-47a6-411e-b7ec-ef793203f836
