cwp() {
    package="$1"
    if [ -z "$package" ]; then
        echo "Specify a package name please!"
        return 1
    fi

    IFS=':' read -ra paths <<< "$ROSWS"
    for path in "${paths[@]}"; do
        if [ -d "$path/src/$package" ]; then
            pkg_path="$(realpath "$path/src/$package")"
            cd "$pkg_path" || return 1
            return 0
        fi
    done

    echo "Package not found."
    return 1
}
