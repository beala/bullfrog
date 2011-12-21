import sys
import argparse

import parse
import declassify
import p3uniquify
import p3explicate
import p3heapify
import p3closure
import p3flattener
import tailcallanalysis
import Myx86Selector
import InterferenceGraph
import p3removestructuredcontrolflow

class Compiler(object):

    compiled = None
    inFilename = None
    outFilename = None

    def __init__(self, in_filename, out_filename):
        self.inFilename = in_filename
        self.outFilename = out_filename

    def compile(self):
        stages = [parse.Parse(),
                  declassify.Declassify(),
                  p3uniquify.P3Uniquify(),
                  p3explicate.P3Explicate(),
                  p3heapify.P3Heapify(),
                  p3closure.P3Closure(),
                  p3flattener.P3ASTFlattener(),
                  tailcallanalysis.TailCallAnalysis()]

        stage_input = self.inFilename
        for stage in stages:
            stage.setInput(stage_input)
            stage_output = stage.do()
            stage_input = stage_output
#        self.compiled = stage_output

        asmString = ""
        data_section = ""
        for func in stage_output:
            selector = Myx86Selector.Myx86Selector()
            tmpIR = selector.generate_x86_code(func)
            data_section += selector.dataSection
            ig = InterferenceGraph.InterferenceGraph(tmpIR)
            coloredIR=ig.allocateRegisters()
            no_ifs = p3removestructuredcontrolflow.P3RemoveStructuredControlFlow().removeIfs(coloredIR)
            ig.setIR(no_ifs)
            asmString += ig.emitColoredIR()
        self.compiled =  "\n"+ data_section +"\n.text"+asmString

    def write(self):
        out_file = open(self.outFilename, "w")
        out_file.write(str(self.compiled))
        out_file.close()

    def setFlags(self, flags):
        pass

    def setOutFile(self, filename):
        self.outFilename = filename

if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser(description="A Toy Python Compiler")
    arg_parser.add_argument(
                'input_file',
                help='The python file to be compiled.')
    arg_parser.add_argument(
                'output_file', 
                nargs="?", 
                default='out.s',
                help='The filename of the compiled program.')
    arg_parser.add_argument(
                '-O',
                action='store_true',
                help='Enable optimizations.')
    options = arg_parser.parse_args()

    compiler = Compiler(options.input_file, options.output_file)
    compiler.compile()
    compiler.write()
