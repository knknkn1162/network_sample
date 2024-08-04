from cmlmag.cml import Cml
import ini as ini
import time

def main():
    cml = Cml()
    lab = cml.lab

    r0 = lab.create_iosv(ini.iosv_0.__name__, 200, 700, slots=1)
    #r1 = lab.create_iosv(ini.iosv_1.__name__, 200, 700, slots=1)
    s0 = lab.create_unmanaged_switch(ini.sw_0.__name__, 500, 400, slots=3)
    # client
    c0 = lab.create_server(ini.server_0.__name__, 200, 400, slots=1)
    ex0 = lab.create_external_connector(ini.ex_0.__name__, 800, 100)
    c1 = lab.create_ubuntu_server(ini.ubuntu_0.__name__, 800, 400, slots=2)

    c0.create_links([s0[1]])
    c1.create_links([ex0[0], s0[0]])
    r0.create_links([s0[2]])
    s0.create_links([c1[1], c0[0], r0[0]])

    lab.start(is_sync=True)

    # print nodes and interfaces states:
    lab.print_nodes()

if __name__ == '__main__':
    main()