from setuptools import find_packages, setup

package_name = "battery_qa"

setup(
    name=package_name,
    version="0.1.0",
    packages=find_packages(exclude=["test"]),
    data_files=[
        ("share/ament_index/resource_index/packages", ["resource/" + package_name]),
        ("share/" + package_name, ["package.xml"]),
    ],
    install_requires=["setuptools"],
    zip_safe=True,
    maintainer="Jongsoo Yang",
    maintainer_email="noreply@example.com",
    description="Fictional ROS 2 battery topic QA exercise",
    license="MIT",
    entry_points={
        "console_scripts": [
            "battery_publisher = battery_qa.battery_nodes:publisher_main",
            "battery_monitor = battery_qa.battery_nodes:monitor_main",
        ],
    },
)
