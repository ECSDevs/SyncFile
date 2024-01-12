#include <iostream>
#include <thread>
#include <cstdlib>

void runProgram(const std::string& programName) {
    std::system(programName.c_str());
}

int main() {
    std::thread t1(runProgram, "mcsmtGo");
    std::thread t2(runProgram, "mcsmtElectronUi");

    return 0;
}