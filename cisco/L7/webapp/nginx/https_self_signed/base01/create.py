from cmlmag.cml import Cml
import ini as ini
import time

def main():
    cml = Cml()
    lab = cml.lab

    ex0 = lab.create_external_connector(ini.ex_0.__name__, 800, 100)
    c0 = lab.create_ubuntu_server(ini.ubuntu_0.__name__, 800, 400, slots=2)

    #s0 = lab.create_unmanaged_switch(ini.sw_0.__name__, 500, 400, slots=2)
    # client
    #c1 = lab.create_ubuntu_server(ini.ubuntu_1.__name__, 200, 400, slots=2)
    #ex1 = lab.create_external_connector(ini.ex_1.__name__, 200, 100)

    ex0.create_links([c0[0]])
    c0.create_links([ex0[0]])
    # c0.create_links([ex0[0], s0[0]])
    # s0.create_links([c0[1], c1[1]])
    
    # ex1.create_links([c1[0]])
    # c1.create_links([ex1[0], s0[1]])

    lab.start(is_sync=True)

    # print nodes and interfaces states:
    lab.print_nodes()

if __name__ == '__main__':
    main()