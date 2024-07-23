from cmlmag.cml import Cml
import ini as ini
import time

def main():
    cml = Cml()
    lab = cml.lab

    s0 = lab.create_unmanaged_switch(ini.sw_0.__name__, 500, 200, slots=2)

    c0 = lab.create_ubuntu_server(ini.ubuntu_0.__name__, 200, 500, slots=1)
    c1 = lab.create_ubuntu_server(ini.ubuntu_1.__name__, 800, 500, slots=2)

    ex0 = lab.create_external_connector(ini.ext_conn0.__name__, 1000, 500)


    ex0.create_links([c1[0]])
    c1.create_links([ex0[0], s0[0]])
    c0.create_links([s0[1]])
    s0.create_links([c1[1], c0[0]])
    # for avoiding timeout in ubuntu
    lab.start(wait_time=120)

    # print nodes and interfaces states:
    lab.print_nodes()

if __name__ == '__main__':
    main()