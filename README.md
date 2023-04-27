# Neurograph
Neural network graph plotter for TensorFlow training data (i.e. GPT-2)

`term_plot.py` - terminal window version

Tested on Windows Git Bash & Ubuntu Linux 22.04LTS

requirements:

`pip install termplotlib`
(termplotlib might have other dependencies)

1. assumes you have your readouts under `logs/`, fetches the latest .txt from that directory
2. prints out a neat graph into your terminal window
3. ???
4. yes

Can be run in an auto-update mode like so in i.e. bash;

```
function termplotview() {
  while true; do
    python term_plot.py
  done
}
```

# TL;DR

The script parses the training data and plots a graph using termplotlib. The x-axis represents the number of iterations, and the y-axis represents the average loss.

Neurograph might be an useful tool for quickly visualizing the training progress of neural networks without having to switch to a separate visualization tool or library. It is also lightweight and does not require a graphical user interface.

