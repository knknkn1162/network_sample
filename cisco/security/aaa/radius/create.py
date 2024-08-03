from cmlmag.cml import Cml
import ini as ini
import time

def main():
    cml = Cml()
    lab = cml.lab

    r0 = lab.create_iosv(ini.iosv_0.__name__, 700, 400, slots=2)
    s0 = lab.create_unmanaged_switch(ini.sw_0.__name__, 400, 400, slots=2)
    # server
    c0 = lab.create_ubuntu_server(ini.ubuntu_0.__name__, 1000, 400, slots=2)
    # client
    c1 = lab.create_ubuntu_server(ini.ubuntu_1.__name__, 100, 400, slots=1)
    ex0 = lab.create_external_connector(ini.ex_conn0.__name__, 1000, 700)

    c1.create_links([s0[0]])
    s0.create_links([c1[0], r0[0]])
    r0.create_links([s0[1], c0[1]])

    c0.create_links([ex0[0], r0[1]])
    ex0.create_links([c0[0]])
    lab.start(is_sync=True)

    # print nodes and interfaces states:
    lab.print_nodes()

if __name__ == '__main__':
    main()