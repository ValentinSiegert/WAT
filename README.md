# Web Agents controlling Things (WAT)

We present a prototype of a yogurt production line that allows autonomous agents to reason on knowledge graphs,
perceive, decide and act for reaching their goals as part of the All The Agents Challenge at ISWC'21.

## Getting Started

1. Setup Pipenv
    ```
    pipenv install
   ```
2. Place Linked Data-FU files in `./ldfu/prog/` such that the executables are findable 
at `./ldfu/prog/bin/ldfu.bat` and `./ldfu/prog/bin/ldfu.sh`.
We tested it only with the standalone version 0.9.13 of Linked Data-Fu,
but also other versions should work.
WAT detects then itself which executable to run based on the used operating system.
The project directory should afterwards look similar to this:
   ```
    project root
    |--- agents
    |--- artifacts
    |--- ldfu
    |    |--- prog # includes now standalone version 0.9.13 of Linked Data-Fu
    |    |    |--- bin
    |    |    |    |--- some shell files
    |    |    |    |--- ldfu.bat
    |    |    |    |--- ldfu.sh
    |    |    |    |--- some more shell files
    |    |    |--- conf
    |    |    |--- doc
    |    |    |--- examples
    |    |    |--- lib
    |    |    |--- ruleset
    |    |    |--- LICENSE.txt
    |    |    |--- README.md
    |    |--- several SPARQL files (*.rq)
    |--- project root files
   ``` 
3. Run program via 
   
    ```
    python main.py
   ```

## Main Contributors

The two main contributors to this repo are:
- [Valentin Siegert](https://vsr.informatik.tu-chemnitz.de/people/siegert)
- [Mahda Noura](https://vsr.informatik.tu-chemnitz.de/people/mahdanoura)

## Acknowledgement

We would like to thank the developers of [Linked Data-FU](https://linked-data-fu.github.io/).
Further, the organizers of the [AI4Industry Summer School 2021](https://ai4industry2021.sciencesconf.org/)
for providing the simulation of the industry use case which was used in this solution.