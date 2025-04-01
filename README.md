# Sistema Gráfico Interativo (SGI)

### Alunos
Eduardo Achar - 23102448
Victoria Rodrigues Veloso - 23100460

### Turma
INE5420-05208 (20251) - Computação Gráfica

## Mudanças efetuadas

Para a segunda entrega do SGI, foram realizadas pequenas melhorias na interface gráfica, conforme ilustrado na imagem abaixo. Entre as alterações, além da atualização das cores, foi adicionada uma barra de rolagem para facilitar a navegação no display.


<div style="text-align: center;">
    <img src="./assets/novamain.png">
    <p style="font-style: italic; font-size: 12px;"></p>
</div>




## Novas funcionalidades

Nesta etapa, o sistema gráfico incorpora as seguintes transformações 2D:  

- **Translação**  
- **Escalonamento** “natural” em torno do centro do objeto  
- **Rotações**, que podem ocorrer em:  
  - Torno do centro do mundo  
  - Torno do centro do objeto  
  - Torno de um ponto arbitrário  

Essas funcionalidades estão demonstradas na figura abaixo:

<div style="text-align: center;">
    <img src="./assets/transformwindow.png">
    <p style="font-style: italic; font-size: 12px;"></p>
</div>

Para aplicar uma transformação a um objeto, é necessário inserir seu nome na caixa **"Name"** da tela inicial e, em seguida, selecionar o botão **"Transform Object"**.  

Além disso, foi adicionada a opção de selecionar uma cor para o objeto gráfico. Ao acionar o botão **"Set Color"**, a interface exibida abaixo será apresentada ao usuário.

<div style="text-align: center;">
    <img src="./assets/colorwindow.png">
    <p style="font-style: italic; font-size: 12px;"></p>
</div>

## Instalação de dependências 

Para a execução do código com as dependêcias necessárias, um requirements.txt foi disponibilizado e pode ser instalado através do comando: 

```sh
pip install -r requirements.txt
```

## Como Executar  
Para executar o programa, dentro da pasta raiz, é possível executar o makefile com o comando abaixo:


```sh
make
```



## Exemplos de entrada



Coordenadas de exemplo para a criação de um ponto:
 ```
 (500,-500)
 ```
Coordenadas de exemplo para a criação de uma reta:


```
(900,-600),(200,-600) 
```

Coordenadas de exemplo para a criação de um polígono:

 ```
(100,-100), (200,-100), (200, -200), (100, -200)
 ```