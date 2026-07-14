# Firmware

Firmware em MicroPython utilizado no projeto escolar de física desenvolvido para demonstrar como uma asa de avião gera sustentação.

O firmware é executado em um ESP32 e mede a velocidade de rotação de dois anemômetros personalizados posicionados acima e abaixo de uma asa impressa em 3D.

## Visão geral

Cada anemômetro utiliza um encoder incremental do tipo through-bore, com dois canais em quadratura chamados **A** e **B**.

O ESP32 detecta as transições dos dois canais, calcula a velocidade de rotação em rotações por minuto e envia as medições para o computador por meio da conexão serial USB.

Os anemômetros são posicionados da seguinte forma:

* **Encoder inferior:** mede o fluxo de ar abaixo da asa.
* **Encoder superior:** mede o fluxo de ar acima da asa.

O software executado no computador pode utilizar essas medições para calcular:

* velocidade do fluxo de ar;
* diferença de pressão;
* força de sustentação estimada;
* gráficos experimentais em tempo real.

## Hardware

O firmware foi desenvolvido para os seguintes componentes:

* ESP32-WROOM-32D;
* dois encoders incrementais through-bore;
* dois anemômetros personalizados;
* quatro resistores pull-up de `10 kΩ`;
* cabo USB para alimentação e comunicação serial.

## Pinagem padrão

| Componente       | Sinal   | GPIO do ESP32 |
| ---------------- | ------- | ------------: |
| Encoder inferior | Canal A |       GPIO 14 |
| Encoder inferior | Canal B |       GPIO 27 |
| Encoder superior | Canal A |       GPIO 32 |
| Encoder superior | Canal B |       GPIO 33 |

A pinagem pode ser alterada no arquivo `config.py`.

```python
ENCODER_BOTTOM_A = 14
ENCODER_BOTTOM_B = 27

ENCODER_TOP_A = 32
ENCODER_TOP_B = 33
```

## Decodificação em quadratura

Os encoders geram dois sinais digitais com aproximadamente 90 graus de defasagem.

Comparando os canais A e B, o firmware consegue determinar:

* quantidade de transições;
* velocidade de rotação;
* sentido da rotação.

O firmware conta as bordas de subida e descida dos dois canais. Esse método é conhecido como decodificação em quadratura **×4**.

A quantidade de contagens por volta é calculada por:

```text
CPR = PPR × 4
```

Onde:

* `PPR` representa a quantidade de pulsos por volta em um canal;
* `CPR` representa a quantidade total de transições detectadas por volta.

## Cálculo de RPM

A velocidade de rotação é calculada por:

```text
RPM = (N × 60) / (CPR × Δt)
```

Onde:

* `N` é a quantidade de contagens do encoder;
* `CPR` é a quantidade de contagens por volta;
* `Δt` é o intervalo de medição em segundos.

Como o firmware utiliza decodificação em quadratura ×4:

```text
RPM = (N × 60) / (4 × PPR × Δt)
```

## Configuração

As configurações principais estão localizadas em `config.py`.

```python
PPR = 1000
QUADRATURE_MULTIPLIER = 4
SAMPLE_INTERVAL_MS = 500
DECIMAL_PLACES = 2
MAX_VALID_RPM = 20000.0
```

### PPR do encoder

A configuração inicial utiliza:

```python
PPR = 1000
```

Esse valor deve ser substituído pelo PPR real informado na documentação do encoder.

Caso o PPR esteja incorreto, o valor calculado de RPM também estará incorreto.

### Intervalo de medição

O intervalo padrão é:

```python
SAMPLE_INTERVAL_MS = 500
```

Isso significa que uma nova medição é enviada a cada `0,5` segundo.

Um intervalo menor gera atualizações mais rápidas, mas pode aumentar a variação das medições em velocidades baixas.

Um intervalo maior gera medições mais estáveis, mas reduz a frequência de atualização.

## Saída serial

O firmware envia as medições em um formato simples separado por vírgula:

```text
rpm_bottom,rpm_top
```

Exemplo:

```text
320.45,391.27
```

Nesse exemplo:

* o anemômetro inferior está girando a `320,45 RPM`;
* o anemômetro superior está girando a `391,27 RPM`.

As linhas iniciadas por `#` contêm mensagens de inicialização ou informações de status:

```text
# Airfoil Lift Experiment
# format: rpm_bottom,rpm_top
320.45,391.27
325.12,397.84
```

O programa executado no computador deve ignorar linhas iniciadas por `#`.

## Visualizando as medições

Utilizando `mpremote`:

```bash
mpremote repl
```

Utilizando um terminal serial:

```bash
python -m serial.tools.miniterm COM3 115200
```

No Linux, a porta serial pode aparecer como:

```text
/dev/ttyUSB0
```

No Windows, pode aparecer como:

```text
COM3
```

A porta exata depende do computador utilizado.

## Sentido de rotação

Como a decodificação em quadratura identifica o sentido da rotação, os valores de RPM podem ser positivos ou negativos.

Caso um anemômetro produza valores negativos durante o fluxo normal de ar, você pode:

* trocar fisicamente os canais A e B;
* trocar os pinos dos canais no `config.py`;
* inverter o sinal no software executado no computador.

O módulo da medição continuará válido desde que o encoder esteja sendo decodificado corretamente.

## Limitações experimentais

O firmware calcula a velocidade de rotação utilizando os pulsos dos encoders, mas o valor de RPM não representa diretamente a velocidade real do ar.

A relação entre RPM e velocidade do fluxo depende de fatores como:

* geometria das hélices ou copos;
* raio do anemômetro;
* atrito mecânico;
* resistência do encoder;
* turbulência;
* perdas mecânicas;
* calibração.

Para medições mais precisas, os anemômetros devem ser calibrados utilizando uma velocidade de ar conhecida.

O modelo físico atual utiliza velocidades médias representativas, medidas em pontos fixos acima e abaixo da asa.

## Autores

* Diego Trigo Araujo
* Luis Felipe Nascimento de Freitas

Projeto escolar de física desenvolvido no Instituto Alpha Lumen.
