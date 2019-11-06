from cx_Freeze import setup, Executable

setup(
    name="TEST_SDK",
    version="0.1",
    description="sdk tester",
    options={
        "build_exe": {
            "packages": ["requests"],
            "include_files": ["./../sdk"]
        }
    },
    executables=[
        Executable(
            script=r"test.py",
            base="Win32GUI",
        )
    ]
)
