from cmlmag.cml import Cml
import ini as ini
import time

def main():
    cml = Cml()
    lab = cml.lab

    s0 = lab.create_unmanaged_switch(ini.sw_0.__name__, 500, 500, slots=3)
    ex0 = lab.create_external_connector(ini.ex_0.__name__, 800, 1000)
    c0 = lab.create_ubuntu_server(ini.ubuntu_0.__name__, 800, 700, slots=2)
    c1 = lab.create_ubuntu_server(ini.ubuntu_1.__name__, 600, 700, slots=2)
    ex1 = lab.create_external_connector(ini.ex_1.__name__, 600, 1000)
    # client
    c2 = lab.create_ubuntu_server(ini.ubuntu_2.__name__, 500, 100, slots=2)

    s0.create_links([c0[1], c1[1], c2[0]])
    c2.create_links([s0[2]])
    ex0.create_links([c0[0]])
    c0.create_links([ex0[0], s0[0]])

    ex1.create_links([c1[0]])
    c1.create_links([ex1[0], s0[1]])

    lab.start(is_sync=True)

    # print nodes and interfaces states:
    lab.print_nodes()

if __name__ == '__main__':
    main()