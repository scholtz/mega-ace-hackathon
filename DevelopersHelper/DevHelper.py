import json
import hashlib


def GenerateTEAL(filename : str):
    #...
    out = "#pragma version 8\n"
    out += "txn NumAppArgs\n"
    out += "int 0\n"
    out += "==\n"
    out += "bnz no_args\n"
    
    # Open the JSON file
    with open(filename, 'r') as f:
        # Load the contents of the file as JSON
        data = json.load(f)
        call_configs={}
        code={}
        # Iterate over each item in the JSON data
        for Interfaces in data['Interfaces']:
            for method in Interfaces['methods']:
                # get abi method name
                name=method['name']
                methodAbi = name+"("
                for args in method['args']:
                    methodAbi += args['type']+","
                methodAbi += ")" + method['returns']['type']
                methodAbi = methodAbi.replace(",)",")")
                #print("methodAbi",methodAbi)
                out += "// method "+methodAbi+"\n"
                out += "txna ApplicationArgs 0\n"
                out+="method \""+methodAbi+"\"\n"
                out += "==\n"
                out += "bnz "+name+"_call_config\n"
                # call_configs
                call_configs[name] = name+"_call_config:\n"
        
                for config in method['call_config']:
                    if 'ApplicationID' in config:
                        call_configs[name]+="txn ApplicationID // "+config['ApplicationID']+"\n"
                        call_configs[name]+="int "+config['ApplicationID'][3:].strip()+"\n"
                        if(config['ApplicationID'][0] == "n"):
                            call_configs[name]+="!=\n"
                        else:
                            call_configs[name]+="==\n"
                        call_configs[name]+="assert\n\n"

                    if 'OnCompletion' in config:
                        call_configs[name]+="txn OnCompletion // "+config['OnCompletion']+"\n"
                        call_configs[name]+="int "+config['OnCompletion'][3:].strip()+"\n"
                        if(config['OnCompletion'][0] == "n"):
                            call_configs[name]+="!=\n"
                        else:
                            call_configs[name]+="==\n"
                        call_configs[name]+="assert\n\n"

                    if 'Sender' in config:
                        call_configs[name]+="txn Sender // "+config['Sender']+"\n"
                        call_configs[name]+="addr "+config['Sender'][3:].strip()+"\n"
                        if(config['Sender'][0] == "n"):
                            call_configs[name]+="!=\n"
                        else:
                            call_configs[name]+="==\n"
                        call_configs[name]+="assert\n\n"

                    if 'RekeyTo' in config:
                        call_configs[name]+="txn RekeyTo // "+config['RekeyTo']+"\n"
                        call_configs[name]+="addr "+config['RekeyTo'][3:].strip()+"\n"
                        if(config['RekeyTo'][0] == "n"):
                            call_configs[name]+="!=\n"
                        else:
                            call_configs[name]+="==\n"
                        call_configs[name]+="assert\n\n"


                call_configs[name] += "b "+name+"_code\n"
                code[name] = name+"_code:\n"
                code[name] += "int 1 // IMPLEMENT CODE HERE\n"
                code[name] += "return\n\n"

        if('supportsInterface' in code):
    
            supportsInterfaceName = 'supportsInterface'
            code[supportsInterfaceName] = "supportsInterface_code:\n"

            xor = ""

            for Interfaces in data['Interfaces']:
                for method in Interfaces['methods']:
                    # get abi method name
                    name=method['name']
                    methodAbi = name+"("
                    for args in method['args']:
                        methodAbi += args['type']+","
                    methodAbi += ")" + method['returns']['type']
                    methodAbi = methodAbi.replace(",)",")")
                    code[supportsInterfaceName] += "txna ApplicationArgs 1\n"
                    code[supportsInterfaceName] +=  "method \""+methodAbi+"\"\n"
                    code[supportsInterfaceName] +=  "==\n"
                    code[supportsInterfaceName] +=  "bnz success\n"
                    if (len(xor) > 0):
                        xor += "method \""+methodAbi+"\"\n"
                        xor += "b^\n"
                    else:
                        xor += "method \""+methodAbi+"\"\n"

            xor = "txna ApplicationArgs 1 //arc-0073 xor implementation https://github.com/algorandfoundation/ARCs/blob/main/ARCs/arc-0073.md#how-interfaces-are-identified\n" +xor+"==\nbnz success\n"
            code[supportsInterfaceName] += xor + "\n\n"
            code[supportsInterfaceName] += "err\n\n"

        out += "err // if no methods found, fail request\n\n"
        out += "return\n"
        out += "no_args:\n"
        out += "err // if app create without args should be implemented it should be placed here\n\n"
        
        for configPart in call_configs:
            out+=call_configs[configPart]+"\n"
        for codePart in code:
            out+=code[codePart]+"\n"
        out += "success:\n"
        out += "int 1\n"

            
    return out  #should return your generated TEAL code

print(GenerateTEAL('Test1.json'))
