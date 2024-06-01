<div align="center">
<h1>Embedded Utils</h1>
<p>CLI Program for Embedded Programming Utils</p>
</div>

# Introdução
Embedded Utils é uma biblioteca projetada com funcionalidades simples mas que podem auxiliar o usuário quando estiver trabalhando com projetos de **Sistemas Embarcados**

## Comandos disponíveis
### `embedded-utils`

**Usage**:

```console
$ embedded-utils [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--install-completion`: Install completion for the current shell.
* `--show-completion`: Show completion for the current shell, to copy it or customize the installation.
* `--version`: Show program version and exit.
* `--help`: Show this message and exit.

**Commands**:

* `informations`
* `mikroc-setup`
* `pic-mcus`
* `showports`

#### `embedded-utils informations`

**Usage**:

```console
$ embedded-utils informations [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

#### `embedded-utils mikroc-setup`

**Usage**:

```console
$ embedded-utils mikroc-setup [OPTIONS]
```

**Options**:

* `--project-name TEXT`: Nome do projeto no MikroC  [required]
* `--help`: Show this message and exit.

#### `embedded-utils pic-mcus`

**Usage**:

```console
$ embedded-utils pic-mcus [OPTIONS]
```

**Options**:

* `--name TEXT`: O nome do MCU a ser pesquisado  [required]
* `--help`: Show this message and exit.

#### `embedded-utils showports`

**Usage**:

```console
$ embedded-utils showports [OPTIONS]
```

**Options**:

* `--show-ports / --no-show-ports`: [default: show-ports]
* `--help`: Show this message and exit.
