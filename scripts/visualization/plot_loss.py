import json
import os
import matplotlib.pyplot as plt
import argparse

def plot_losses(jsonl_filepath, output_dir, script_name):
    epochs = []
    train_losses = []
    val_losses = []

    with open(jsonl_filepath, 'r') as file:
        for line in file:
            data = json.loads(line)
            epochs.append(data["epoch"])
            train_losses.append(data["train_loss"])
            val_losses.append(data["val_loss"])

    plt.figure(figsize=(10, 6))
    plt.plot(epochs, train_losses, label="Train Loss", marker='o')
    plt.plot(epochs, val_losses, label="Validation Loss", marker='o')
    plt.xlabel("Epoch")
    plt.ylabel("Loss")
    plt.title("Training and Validation Loss")
    plt.legend()
    plt.grid(True)

    output_path = os.path.join(output_dir, f"visualization/{script_name}.pdf")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path)
    plt.close()
    print(f"Plot saved to {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Plot training and validation loss.")
    parser.add_argument(
        "--log_dir",
        type=str,
        required=True,
        help="Directory containing log.jsonl",
    )
    args = parser.parse_args()

    jsonl_filepath = os.path.join(args.log_dir, "log.jsonl")
    assert os.path.exists(jsonl_filepath), f"log.jsonl not found in {args.log_dir}"

    script_name = os.path.splitext(os.path.basename(__file__))[0] 
    plot_losses(jsonl_filepath, args.log_dir, script_name)
