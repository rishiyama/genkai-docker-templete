import os
import yaml
from glob import glob
from natsort import natsorted

def generate_overview(base_dir):
    overview_path = os.path.join(base_dir, "overview.log")
    config_paths = glob(os.path.join(base_dir, "*output*/**/config.yaml"), recursive=True)
    config_paths = natsorted(config_paths, key=lambda y: os.path.basename(os.path.dirname(y)))[::-1]

    with open(overview_path, "w") as overview_file:
        for config_path in config_paths:
            experiment_dir = os.path.dirname(config_path)
            overview_file.write("-" * 50 + "\n")
            overview_file.write(f"# Experiment: {experiment_dir}\n")
            
            
            with open(config_path, "r") as config_file:
                config = yaml.safe_load(config_file)
                for key, value in config.items():
                    overview_file.write(f"{key}: {value}\n")
            
            overview_file.write("\n")
    print(f"Overview written to {overview_path}")

if __name__ == "__main__":
    base_dir = "."
    generate_overview(base_dir)
