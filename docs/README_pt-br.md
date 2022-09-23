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
    * 🆕 [Autenticação com usuário e senha](#auth-with-user-and-pass)
  * [Como configurar o bot](#how-config-bot)
    * [Quais são os problemas](#what-are-problems)
    * [Threshold no arquivo de configuração](#threshold-config)
    * [Substituição das imagens targets](#image-replacement)
    * [Alguns comportamentos que podem indicar um falso positivo ou negativo](#some-behaviors)

## 📋 <a id="about"></a>Sobre

Este bot contêm códigos de outros desenvolvedores, esse bot foi somente refatorado, para facilitar novas implementações e manutenções.  

Desenvolvedores (Código base):
* https://github.com/mpcabete/
* https://github.com/vin350/ (Telegram integração)

Este bot é grátis e de código aberto.

Recursos:  
* Refatoração do código
* Adicionado os 3 captchas
* Temas
* Multi conta com janelas lado a lado e muitas janelas maximizadas
* Rodar o Bot, sem interrupção por erro
* Terminal colorido
* Velocidade no Bot, ganho de alguns minutos nas tarefas
* Atualização obrigatório do arquivo de configuração
* Atualização automática dos arquivos (requer o Git instalado)
* Relatório de Bcoins, depois de finalizar o mapa
* Novas estimativa do mapa adicionada
* Novos comandos no Telegram (workall, restall)
* Multi contas com Multi autenticação
* Envia os heróis para a **Casa** por raridade

## 🎁 <a id="donation"></a>Doação
BCOIN: 0x4847C29561B6682154E25c334E12d156e19F613a  
SEN: 0x4847C29561B6682154E25c334E12d156e19F613a  
PIX: 08912d17-47a6-411e-b7ec-ef793203f836  

## 🤖 <a id="robot-preview"></a>Robô - Previsualização
![Screenshot - Preview](https://raw.githubusercontent.com/newerton/bombcrypto-bot/main/images/readme/bot_working.png)

## 🪟 <a id="installation"></a>Instalação

### **Python**

🖥️ Computador/Notebook com Alto e Média configuração  
🐍 Instalar o Python 3.9.9

🖥️ Computador/Notebook com Baixa configuração or baixa configuração com Windows 7 Pro  
🐍 Instalar o Python 3.8.10

🔗 [https://www.python.org/downloads/](https://www.python.org/downloads/)

⚠️ **É importante marcar a opção para adicionar o python ao PATH**  

### **Git (Para usar o auto-update)**

Windows: [https://gitforwindows.org/](https://gitforwindows.org/)  
Linux (Ubuntu): sudo apt -y update && sudo apt -y install git

⚠️ **Abra um novo terminal e digite o comando abaixo, para verificar se foi instalado corretamente**
```
git version
```

### <a id="commands"></a>Commands
Instale as dependências, executando o comando abaixo, dentro da pasta do projeto:  

```
pip install -r requirements.txt
```
Pronto! Agora é só iniciar o bot com o comando, dentro da pasta do projeto  

```
python index.py
```
| comandos | sistema operacional | descrição |
| :---: | :---: | :---: |
| ./cmd/update_files.sh | Linux	| Atualiza todos os arquivos, menos o config.yaml and telegram.yaml and atualiza o requirements.txt do Python |
| ./cmd/update.sh | Linux	| Atualiza somente o requirements.txt do Python |
| .\cmd\update_files.bat | Windows | Atualiza todos os arquivos, menos o config.yaml and telegram.yaml and atualiza o requirements.txt do Python |
| .\cmd\update.bat | Windows | Atualiza somente o requirements.txt do Python |



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
| game | string | amazon_survival |
| verify_version | boolean - true/false | Verificar a versão do app a cada 1h, recomendado para manter atualizado |
| emoji | boolean - true/false | Ativar/Desativar mostrar emoji nas mensagens do console |
| terminal_colorful | boolean - true/false | Ativar/Desativar mostrar mensagens coloridas no terminal |
| run_time_app |  int | Tempo de execução do loop do bot |
| monitor_to_use | int | Monitor que o bot usa como referência |
| captcha |  boolean - true/false | Ativar/Desativar o reconhecimento do captcha no jogo |
| speed | string - normal/fast | Dois modos de velocidade do bot, o modo fast é entre 1~3 minutos mais rápido |
| authenticate | boolean - true/false | Ativar/Desativar o login com usuário e senha |
| **multi_account** | - | - |
| enable | boolean - true/false | Ativar/Desativar a funcionalidade de Multi Account  |
| window_title | string | Título da janela, para identificação do jogo ativo pelo bot |
| window_fullscreen | boolean - true/false | Ativar/Desativar o modo Fullscreen, recomendado para monitores pequenos |
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
| work_button | decimal | Valor de confiança do botão de WORK |
| home_enable_button | decimal | Valor de confiança do botão de HOME habilitado |
| heroes_green_bar | decimal | Valor de confiança da barra verde parcial de energia do herói |
| heroes_red_bar | decimal | Valor de confiança da barra vermelha parcial de energia do herói |
| heroes_full_bar | decimal | Valor de confiança da barra completa de 
energia do herói |
| heroes_send_all | decimal | Valor de confiança do botão de enviar todos para trabalhar |
| heroes_rest_all | decimal | Valor de confiança do botão de enviar todos para descansar |
| chest | decimal | Valor de confiança dos baús, para calcular o total de tokens do mapa |
| jail | decimal | Valor de confiança dos baús, para calcular o total de jaula do mapa |
| auth_input | decimal | Valor de confiança do campo de login |
| heroes.common | decimal | Valor de confiança da tag de raridade - common |
| heroes.rare | decimal | Valor de confiança da tag de raridade - rare |
| heroes.super_rare | decimal | Valor de confiança da tag de raridade - super_rare |
| heroes.epic | decimal | Valor de confiança da tag de raridade - epic |
| heroes.legend | decimal | Valor de confiança da tag de raridade - legend |
| heroes.super_legend | decimal | Valor de confiança da tag de raridade - super_legend |
| **heroes** | - | - |
| mode | string - all, green, full | Modo de enviar os heróis para o trabalho.<br />**all** - Envia todos os heróis, sem critério.<br />**green** - Envia os heróis com energia parcialmente verde<br />**full** - Envia os heróis com energia completa|
| **list** | - | - |
| scroll_attempts | int | Total de rolagem que o bot vai fazer na lista de heróis |
| **offsets** | - | - |
| work_button_green | array - [int, int] | Offset para o click do mouse no botão de WORK |
| work_button_full | array - [int, int] | Offset para o click do mouse no botão de WORK |
| **metamask** | - | - |
| enable | boolean - true/false | Ativar/Desativar o auto login da Metamask |
| password | string | Senha para desbloquear a Metamask para logar no jogo |
| **services** | - | - |
| telegram | boolean - true/false | Ativar/Desativar o serviço de envio de mensagem para o Telegram |
| **log** | |
| save_to_file | boolean - true/false | Ativar/Desativar salvar o log do console no arquivo logger.log |
| console | boolean - true/false | Ativar/Desativar a depuração de algumas informações do bot |
| show_print | boolean - true/false | Ativar/Desativar mostrar o printscreen da analise do bot |

## <a id="auth-with-user-and-pass"></a>👥 Autenticação com usuário e senha


### ⚠️ Não esqueça de renomear o arquivo /config/EXAMPLE-accounts.yaml, para /config/accounts.yaml.  


Uma conta sem a Casa
```
1: {username: "seu usuário", password: "sua senha", house: false, rarity: []}
```

Uma conta com a Casa
```
1: {username: "seu usuário", password: "sua senha", house: true, rarity: ["super_rare", "legend"]}
```

Várias contas sem a Casa

```
1: {username: "seu usuário", password: "sua senha", house: false, rarity: []}
2: {username: "seu usuário", password: "sua senha", house: false, rarity: []}
3: {username: "seu usuário", password: "sua senha", house: false, rarity: []}
```

Várias contas com/sem a Casa

```
1: {username: "seu usuário", password: "sua senha", house: true, rarity: ["rare", "super_rare"]}
2: {username: "seu usuário", password: "sua senha", house: false, rarity: []}
3: {username: "seu usuário", password: "sua senha", house: true, rarity: ["super_legend", "legend", "epic"]}
```

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