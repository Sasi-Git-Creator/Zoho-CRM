steps:
  - uses: actions/checkout@v4
    with:
      ref: main
      fetch-depth: 0  # Fetches full history instead of shallow clone
