#include <graylog_logger/Log.hpp>
#include <iostream>

int main() { Log::Msg(Severity::Warning, "42"); }
