from svg2plan.domains.domain import Domain as SVDomain
from svg2plan.generate.main import plot_domains
from svg2plan.generate.setup import create_domain_list
from svg2plan.helpers.layout import DomainsDict
from svg2plan.placement.attract import adjust_domains


def show_domain_plot(domains: list[SVDomain], label=""):
    fig = plot_domains(domains, label=label)
    fig.show(renderer="browser")


def adjust_domains_and_plot(domains_dict: DomainsDict, plot=False):
    layout = adjust_domains(domains_dict)
    domains_list = create_domain_list(layout.domains)

    if plot:
        show_domain_plot(domains_list, label="original")
        show_domain_plot(domains_list, label="adjust domains")

    return layout
