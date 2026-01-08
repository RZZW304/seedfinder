# Contributing to SeedFinder

## Development

### Setup

1. Fork the repository
2. Clone your fork:
```bash
git clone https://github.com/yourusername/seedfinder.git
cd seedfinder
```

3. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

### Code Style

- Follow PEP 8 style guide
- Use descriptive variable names
- Add docstrings to functions and classes
- Keep functions focused and small
- Write clean, readable code

### Commit Guidelines

- Commit messages should be clear and concise
- Use imperative mood: "Add feature" not "Added feature"
- Separate subject from body with blank line
- Limit subject line to 50 characters

Example:
```
Add biome filtering option

Users can now filter results by specific
biomes to find villages in preferred
terrain types.
```

### Testing

Before submitting pull requests:
1. Test the GUI thoroughly
2. Test build process on your platform
3. Verify all features work as expected
4. Check for memory leaks in long-running searches

### Pull Request Process

1. Create a new branch: `git checkout -b feature/your-feature-name`
2. Commit your changes: `git commit -m "Add your feature"`
3. Push to the branch: `git push origin feature/your-feature-name`
4. Create a Pull Request

### Issues

- Use GitHub Issues for bug reports and feature requests
- Include steps to reproduce bugs
- Provide screenshots for GUI issues
- Specify Minecraft version and OS when reporting issues

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
