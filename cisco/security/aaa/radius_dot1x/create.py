from cmlmag.cml import Cml
import ini as ini
import time

def main():
    cml = Cml()
    lab = cml.lab

    s0 = lab.create_unmanaged_switch(ini.sw_0.__name__, 400, 400, slots=2)
    s1 = lab.create_iosvl2(ini.iosvl2_0.__name__, 700, 400, slots=3)

    # server
    c0 = lab.create_ubuntu_server(ini.ubuntu_0.__name__, 1000, 400, slots=2)
    # client
    c1 = lab.create_ubuntu_server(ini.ubuntu_1.__name__, 100, 400, slots=2)

    c2 = lab.create_server(ini.server_0.__name__, 900, 700, slots=1)
    ex0 = lab.create_external_connector(ini.ex_conn0.__name__, 1000, 700)
    ex1 = lab.create_external_connector(ini.ex_conn1.__name__, 100, 700)

    ex1.create_links([c1[0]])
    #c1.create_links([s0[0]])

    c1.create_links([ex1[0], s0[0]])

    s0.create_links([c1[1], s1[0]])
    s1.create_links([s0[1], c0[1], c2[0]])
    # s0.create_links([c1[0], r0[0]])
    # r0.create_links([s0[1], c0[1]])
    c2.create_links([s1[2]])

    c0.create_links([ex0[0], s1[1]])
    ex0.create_links([c0[0]])
    lab.start(is_sync=True)

    # print nodes and interfaces states:
    lab.print_nodes()

if __name__ == '__main__':
    main()