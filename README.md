<h1 align="center">

![Bomb Crypto Banner](https://raw.githubusercontent.com/newerton/bombcrypto-bot/main/images/readme/banner.jpg)

  <a>
    💣 Bomb Crypto Bot 💣 
  </a>
</h1>

## ⚠️ Aviso

Não me responsabilizo por eventuais penalidades sofridas por quem usar o bot, use por sua própria conta e risco.

## 📋 Sobre

Este bot contêm códigos de outros desenvolvedores, esse bot foi somente refatorado, para facilitar novas implementações e manutenções.

Developers:
* https://github.com/mpcabete/
* https://github.com/afkapp/

Este bot grátis e com o código aberto.

My Features:  
* Refactored code
* Add 3 captchas
* Themes
* Multi account with many windows side-by-side or many windows maximized
## 🎁 Wallet
Wallet Smart Chain(BEP20): 0x4847C29561B6682154E25c334E12d156e19F613a  
PIX: 08912d17-47a6-411e-b7ec-ef793203f836  

## 🤖 Robot - Preview
![Screenshot - Preview](https://raw.githubusercontent.com/newerton/bombcrypto-bot/main/images/readme/bot_working.jpg)

## 🪟 Instalação:

🖥️ Computer/Laptop High or Medium Profile  
🐍 Instale o Python 3.9.9

🖥️ Computer/Laptop Low Profile or Low Profile with Windows 7  
🐍 Instale o Python 3.8.10

🔗 [https://www.python.org/downloads/](https://www.python.org/downloads/)


⚠️ **É importante marcar a opção para adicionar o
python ao PATH**

Instale as dependências, executando o comando abaixo, dentro da pasta do projeto:

```
pip install -r requirements.txt
```
Pronto! Agora é só iniciar o bot com o comando, dentro da pasta do projeto

```
python index.py
```

Assim que ele iniciar ele vai começar mandando os bonecos trabalhar. Para que ele funcione é preciso que a janela do game esteja aparecendo na sua tela.
Ele vai constantemente checar se você foi desconectado para realizar o login novamente.

### **Como funciona?**

O bot não interage diretamente com o jogo, ele somente tira print da tela do
game para encontrar os botões e simula movimentos do mouse, isso faz com que
diferenciar o bot de um humano seja muito difícil.

### ⚠️ Algumas configurações podem ser mudadas no arquivo /config/config.yaml, não se esqueça de reiniciar o bot caso mude as configuraçoes.
### ⚠️ Algumas alterações no arquivo /config/config.yaml, pode fazer o bot parar, como por exemplo ativar o telegram quando o bot estiver em execução.

## 🧪 Testes
**Desktop Medium Profile**  
Intel i5-3570k @ 3.4Ghz, 24GB RAM  
Windows 11, Resolution@1920x1080  
Python 3.9.9  

**Laptop Low Profile**  
Laptop Samsumg RV411, Pentium P6200 @ 2.13Ghz, 2GB RAM  
Windows 7, Resolution@1366x768  
Python 3.8.10

## ⚠️ Ajustando o bot

**Por que uns ajustes podem ser necessários?**

O bot usa reconhecimento de imagem para tomar decisões e movimentar o mouse e
clicar nos lugares certos.  
Ele realiza isso comparando uma imagem de exemplo com um screenshot da tela do
computador/laptop.  
Este método está sujeito a inconsistências devido a diferenças na resolução da
sua tela e de como o jogo é renderizado no seu computador.
É provável que o bot não funcione 100% na primeira execução, e que você precise fazer alguns ajustes no arquivo de configuração.

**Quais são os problemas?**

* **Falso negativo** - O bot deveria reconhecer uma imagem, por exemplo, o botão de mandar para trabalhar, mas não reconheceu a imagem na screenshot.

* **Falso positivo** - O bot pensa que reconheceu a imagem que está procurando em um lugar em que esta imagem não aparece.

Para resolver estes problemas existem duas possibilidades, a regulagem do
parâmetro "threshold" no arquivo config.yaml ou a substituição da imagem de
exemplo na pasta "targets" para uma tirada no seu próprio computador:

  ### **Threshold na config**

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

  ### **Substituição das imagens**

  As imagens exemplo são armazenadas na pasta "images/themes/default". Estas imagens foram tiradas no meu computador com resolução de 1920x1080. Para substituir alguma imagem que não esta sendo reconhecida propriamente, simplesmente encontre a imagem correspondente na pasta "images/themes/default",
  tire um screenshot da mesma área e substitua a imagem anterior. É importante
  que a substituta tenha o mesmo nome, incluindo a extensão .png

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

## 🎨 Themes
|      code     	| toolbar image preview 	|
|:-------------:	|:-----:	|
| lunar_newyear 	| ![Lunar New Year](https://raw.githubusercontent.com/newerton/bombcrypto-bot/main/images/readme/themes/lunar_newyear.jpg)	|
## 👍 Curtiu? Dê aquela fortalecida :)

### Wallet Smart Chain(BEP20): 0x4847C29561B6682154E25c334E12d156e19F613a  
### PIX: 08912d17-47a6-411e-b7ec-ef793203f836
