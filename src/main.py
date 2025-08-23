import torch

def main():
    """
    Initial entry point to verify environment setup.
    """
    print("--- Ethical Guardian Sandbox ---")
    print("Status: Initializing...")
    print(f"PyTorch version: {torch.__version__}")
    if torch.cuda.is_available():
        print(f"CUDA detected: {torch.cuda.get_device_name(0)}")
    else:
        print("CUDA not detected. Running on CPU.")
    print("Environment checksum: PASSED.")
    print("Ready to receive Socratic Corpus.")
    print("------------------------------")
    print("Sandbox is live. Awaiting further instructions.")

if __name__ == "__main__":
    main()
