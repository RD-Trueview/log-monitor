from monitor.watcher import load_config, watch_loop

def main():
    cfg = load_config("config.yaml")
    print("Starting Log Monitor...")
    watch_loop(cfg)

if __name__ == "__main__":
    main()
