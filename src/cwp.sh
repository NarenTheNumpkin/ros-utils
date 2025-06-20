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

rpk() {
    PKG_NAME="$1"
    PKG_TYPE="$2"

    if [[ -z "$PKG_NAME" ]]; then
        echo "Specify package name please !"
        return 1
    fi

    if [[ -z "$PKG_TYPE" ]]; then
        ros2 pkg create --build-type ament_python "$PKG_NAME" --dependencies std_msgs geometry_msgs rclpy rclcpp
    else
        ros2 pkg create --build-type ament_"${PKG_TYPE}" "$PKG_NAME" --dependencies std_msgs geometry_msgs rclpy rclcpp
    fi
}