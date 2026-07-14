# bernoulli-principle

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)
[![Documentation: CC BY 4.0](https://img.shields.io/badge/Documentation-CC%20BY%204.0-lightgrey.svg)](./LICENSE-DOCUMENTATION)

[English version](./README_en.md)

Projeto escolar de física desenvolvido para demonstrar como uma asa gera sustentação por meio da análise do fluxo de ar acima e abaixo de um perfil aerodinâmico.

O experimento utiliza uma asa impressa em 3D, dois anemômetros personalizados, encoders incrementais, um ESP32 com MicroPython e um túnel de vento construído com tubo de PVC.

## Visão geral

Dois anemômetros são posicionados em regiões diferentes da asa:

- um acima da superfície superior;
- um abaixo da superfície inferior.

Cada anemômetro é conectado a um encoder incremental. O ESP32 lê os canais em quadratura, calcula a velocidade de rotação em RPM e envia os valores ao computador pela conexão serial USB.

No computador, os dados podem ser utilizados para estimar:

- velocidade do ar;
- diferença de pressão;
- força de sustentação;
- comportamento do fluxo ao redor da asa.

## Funcionamento

```text
Entrada de ar
     ↓
[ Ventilador ]
     ↓
[ Anemômetro superior ]
[          Asa          ]
[ Anemômetro inferior  ]
     ↓
Saída do túnel
```

O ESP32 envia as medições no seguinte formato:

```text
rpm_bottom,rpm_top
```

Exemplo:

```text
312.45,389.21
```

## Componentes principais

- ESP32-WROOM-32D;
- dois encoders incrementais through-bore;
- dois anemômetros de copos impressos em 3D;
- asa experimental impressa em 3D;
- quatro resistores pull-up de `10 kΩ`;
- tubo de PVC com aproximadamente `24 cm` de diâmetro;
- ventilador;
- computador para leitura e processamento dos dados.

## Pastas

- [`firmware/`](./firmware/) — código MicroPython executado no ESP32;
- [`electronics/`](./electronics/) — diagrama esquemático e conexões;
- [`hardware/`](./hardware/) — modelos CAD, arquivos STL e montagem;
- [`software/`](./software/) — leitura serial, cálculos e gráficos;
- [`report/`](./report/) — relatório completo em LaTeX.

## Hardware

O conjunto mecânico possui três elementos principais.

### Asa

A asa apresenta uma superfície superior curva e uma superfície inferior aproximadamente plana.

Os arquivos CAD e STL devem ficar em:

```text
hardware/cad/wing.step
hardware/stl/wing.stl
```

### Anemômetros

Cada anemômetro utiliza três copos distribuídos ao redor de um eixo central conectado a um encoder incremental.

Os arquivos devem ficar em:

```text
hardware/cad/anemometer.step
hardware/stl/anemometer.stl
```

### Túnel de vento

O fluxo de ar é direcionado por um túnel construído com tubo de PVC.

Os arquivos devem ficar em:

```text
hardware/cad/pvc-wind-tunnel.step
hardware/stl/pvc-wind-tunnel.stl
```

Consulte a documentação completa de montagem:

[`hardware/hardware.md`](./hardware/hardware_pt.md)

## Eletrônica

Os dois encoders são conectados ao ESP32 utilizando quatro sinais.

| Sensor | Canal | GPIO |
|---|---|---:|
| Encoder superior | A | GPIO 32 |
| Encoder superior | B | GPIO 33 |
| Encoder inferior | A | GPIO 14 |
| Encoder inferior | B | GPIO 27 |

Cada linha de sinal utiliza um resistor pull-up externo de `10 kΩ` conectado a `3,3 V`.

Consulte o esquema completo:

[`electronics/eletronics.md`](./electronics/eletronics_pt.md)

## Firmware

O firmware em MicroPython:

1. detecta as transições dos canais A e B;
2. realiza a decodificação em quadratura;
3. conta os pulsos dos encoders;
4. calcula a velocidade em RPM;
5. envia os dados pela serial USB.

Consulte:

[`firmware/firmware.md`](./firmware/firmware_pt.md)

## Modelo físico

A velocidade angular é calculada a partir da rotação:

```text
ω = RPM × π / 30
```

A velocidade tangencial aproximada é:

```text
v = ωr
```

A diferença de pressão é estimada utilizando a equação de Bernoulli, considerando as velocidades médias medidas acima e abaixo da asa.

O modelo possui simplificações e representa uma aproximação experimental. Os anemômetros precisam ser calibrados para relacionar corretamente RPM e velocidade real do ar.

## Relatório

O relatório escolar completo apresenta:

- introdução;
- objetivos;
- materiais;
- metodologia experimental;
- princípio de Bernoulli;
- cálculo de RPM;
- diferença de pressão;
- estimativa da sustentação;
- funcionamento dos encoders;
- limitações experimentais;
- resultados;
- conclusão.

Consulte:

[`report/README.md`](./report/report_pt.md)

## Autores

- Diego Trigo Araujo
- Luis Felipe Nascimento de Freitas

Projeto escolar de física desenvolvido no Instituto Alpha Lumen.

## Licença

O código-fonte presente nas pastas `firmware/` e `software/` está licenciado sob a [MIT License](./LICENSE).

O relatório, os modelos CAD, os diagramas e as imagens estão licenciados sob a [Creative Commons Attribution 4.0 International](./LICENSE-DOCUMENTATION).

Ao reutilizar o material, forneça o crédito adequado aos autores.