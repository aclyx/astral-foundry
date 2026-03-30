from pathlib import Path


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    packages_dir = root / "packages"

    # Path objects stay composable and OS-safe in a way stringly-typed path joins do not.
    package_names = sorted(path.name for path in packages_dir.iterdir() if path.is_dir())
    print(f"workspace root: {root}")
    print("packages:", ", ".join(package_names))


if __name__ == "__main__":
    main()
