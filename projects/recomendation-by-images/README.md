# Sistema de recomendação por imagens

Depois de entender o funcionamento de Sistemas de Recomendação e suas aplicações, neste projeto vamos então desenvolver um modelo capaz de classificar imagens por sua similaridade e gerar resultados para o usuário de um site. Os resultados esperados são direcionados para, por meio de um produto buscado na internet, o Sistema de Recomendação deve indicar produtos relacionados, mas não por seus dados textuais (preço, modelo, marca, loja) e, sim, por sua aparência física (formato, cor, textura, etc).

Para que este sistema seja desenvolvido, vamos treinar uma rede de Deep Learning com várias classes de objetos, como por exemplo: relógio, camiseta, bicicleta, sapato, etc.  Dentro de cada classe devemos ter objetos que são parecidos em sua aparência, como pode ser visto na figura a seguir:

![Figura 1: Objetos similares em sua aparência.]("./images/image.png)

Para exemplo, podemos então utilizar o sistema de recomendação por imagens apresentado [aqui](https://colab.research.google.com/github/sparsh-ai/rec-tutorials/blob/master/_notebooks/2021-04-27-image-similarity-recommendations.ipynb)
