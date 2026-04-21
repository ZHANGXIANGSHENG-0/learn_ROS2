from setuptools import find_packages, setup

package_name = 'my_turtle_controller'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='sam',
    maintainer_email='sam@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },

    #注意這裡[]列表負責定義節點的別名與實際檔案路徑的對應關係。
    #它的格式規範：'執行命令 = 包名.檔案名:進入點函數'
    entry_points={
        'console_scripts': [
            'avoid_node = my_turtle_controller.avoidance_node:main'
        ],
    },
)
