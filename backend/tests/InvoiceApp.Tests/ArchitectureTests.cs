using InvoiceApp.Domain;
using Xunit;

namespace InvoiceApp.Tests;

public class ArchitectureTests
{
    [Fact]
    public void DomainAssembly_DoesNotReferenceApiOrAspNetCore()
    {
        var references = typeof(ApprovalService).Assembly.GetReferencedAssemblies();

        Assert.DoesNotContain(references, reference => reference.Name == "InvoiceApp.Api");
        Assert.DoesNotContain(
            references,
            reference => reference.Name is not null &&
                         reference.Name.StartsWith("Microsoft.AspNetCore", StringComparison.Ordinal));
    }
}
